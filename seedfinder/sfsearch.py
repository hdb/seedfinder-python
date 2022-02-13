from seedfinder import SeedFinder
from termcolor import colored
from dotenv import load_dotenv
import os
from difflib import SequenceMatcher
import argparse
import webbrowser

CHAR_LIMIT = 320


def search(sf, query, limit=5, include_breeder_info=False, print_results=False, interactive=False, lucky=False):
    search_results = sf.searchStrain(query)['strains']
    search_results_list = rankResults([v for k,v in search_results.items()], query, key='name')

    if lucky:
        webbrowser.open_new_tab(getDetails(sf,search_results_list,limit=1)[0]['links']['info'])
    elif not interactive:
        detailed_results = getDetails(sf, search_results_list, limit)
        if print_results:
            printResults(detailed_results, include_breeder_info)
            return detailed_results
        else:
            return detailed_results
    else:
        inputHandler(sf, search_results_list, limit, include_breeder_info)

def inputHandler(sf, results, limit, include_breeder_info, page=1):
    detailed = getDetails(sf, results, limit, page)
    printResults(detailed, include_breeder_info)
    user_input = input(colored('Enter result # to open in browser, "n" to get next page or "q" to quit:\n','red'))
    if user_input.lower().startswith('n'):
        print()
        inputHandler(sf, results, limit, include_breeder_info, page+1)

    elif user_input.isdigit():
        entry = int(user_input)-1
        if entry <= len(detailed):
            webbrowser.open_new_tab(detailed[entry]['links']['info'])
    elif user_input.lower().startswith('q'):
        print('exiting...')
        exit()
    else:
        print('exiting...')
        exit()

def getDetails(sf, results, limit, page=1):
    idx_start = (page - 1) * limit
    idx_end = page * limit
    detailed_results = [sf.strainInfo(v['id'], v['brid'], show_parents=True) for v in results[idx_start:idx_end]]
    return detailed_results

def printResults(results, include_breeder_info=False):

    for i, v in enumerate(results):
        # print(v['brinfo'])
        parents_str = v['parents']['info']
        for x,y in v['parents']['strains'].items():
            parents_str = parents_str.replace(x,y['name'])

        print('{header}\n{lineage}\n{body}\n{link}\n'.format(
            header=colored('{idx}. {strain_name} ({breeder_name})'.format(
                idx=i+1,
                strain_name=v['name'],
                breeder_name=v['brinfo']['name']
            ), 'green'),
            lineage=colored('lineage: {}'.format(parents_str), 'cyan'),
            body='{strain_description}\n{breeder_description}'.format(
                strain_description=v['brinfo']['descr'] if len(str(v['brinfo']['descr'])) < CHAR_LIMIT else v['brinfo']['descr'][:CHAR_LIMIT-3]+'...',
                breeder_description=v['brinfo']['description'] if len(str(v['brinfo']['description'])) < CHAR_LIMIT else v['brinfo']['description'][:CHAR_LIMIT-3]+'...'
            ) if include_breeder_info else
            '{strain_description}'.format(
                strain_description=v['brinfo']['descr'] if len(str(v['brinfo']['descr'])) < CHAR_LIMIT else v['brinfo']['descr'][:CHAR_LIMIT-3]+'...',
            ) ,
            link=v['links']['info']
        ))

def rankResults(search_results, search, key):
    return sorted(search_results, key=lambda z: SequenceMatcher(None, z[key], search).ratio(), reverse=True)

def parse():
    parser = argparse.ArgumentParser(description='Search strain on seedfinder')
    parser.add_argument('query', nargs='+',
                        help='search query')
    parser.add_argument('-l', '--limit', nargs='?', type=int, default=5,
                        help='number of results to show. default is 5')
    parser.add_argument('-b', '--breeder-info', action='store_true', default=False,
                        help='include breeder info in results')
    parser.add_argument('-ni', '--not-interactive', action='store_false', default=True,
                        help='don\'t use interactive prompt. print first page of results and exit program')
    parser.add_argument('-L', '--lucky', action='store_true', default=False,
                        help='skip console and open first result in browser')
    return parser.parse_args()

def main():
    load_dotenv()
    args = parse()
    sf = SeedFinder(os.getenv('SF_API_KEY'))
    query = ' '.join(args.query)
    interactive = args.not_interactive
    search(sf, query, limit=args.limit, print_results=True, include_breeder_info=args.breeder_info, interactive=interactive, lucky=args.lucky)

if __name__ == '__main__':
    main()