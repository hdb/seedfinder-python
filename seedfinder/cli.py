from __future__ import annotations

from seedfinder.seedfinder import SeedFinder

from dotenv import load_dotenv
import os
from difflib import SequenceMatcher
import argparse

from rich import print
from rich.panel import Panel
from rich.text import Text

from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4', message='.*input looks.*')


def search(sf, query: str, limit: int = 5, print_results: bool = False, interactive: bool = False) -> None | list[dict]:
    """Make search query and request input"""

    search_results = sf.searchStrain(query)['strains']
    search_results_list = rank_results([v for k,v in search_results.items()], query, key='name')

    if not interactive:
        detailed_results = get_details(sf, search_results_list, limit)
        if print_results:
            print_results(detailed_results)
            return detailed_results
        else:
            return detailed_results
    else:
        input_handler(sf, search_results_list, limit)

def input_handler(sf, results: list[dict], limit: int, page: int = 1) -> None:
    """Process user input"""

    detailed = get_details(sf, results, limit, page)
    print_results(detailed)
    print(Text('Enter "n" to get next page or "q" to quit:\n', style='magenta bold'))
    user_input = input()
    if user_input.lower().startswith('n'):
        print()
        input_handler(sf, results, limit, page+1)
    elif user_input.lower().startswith('q'):
        print('[red]quiting...')
        exit()
    else:
        print('[red]quiting...')
        exit()

def get_details(sf, results: list[dict], limit: int, page: int = 1) -> list[dict]:
    """Return strain result details"""

    idx_start = (page - 1) * limit
    idx_end = page * limit
    detailed_results = [sf.strainInfo(v['id'], v['brid'], show_parents=True) for v in results[idx_start:idx_end]]
    return detailed_results

def print_results(results: list[dict]) -> None:
    """Print results to terminal"""

    for i, v in enumerate(results):
        parents_str = v['parents']['info']
        for x,y in v['parents']['strains'].items():
            parents_str = parents_str.replace(x,y['name'])

        print(
            Panel(
                f"{clean_description(v['brinfo']['descr']) if isinstance(v['brinfo']['descr'], str) else '[red]No description available'}",
                title=f"[green bold]{v['name']}[/] [green]({parents_str})[/] - [bold]{v['brinfo']['name']}",
                title_align='left',
                border_style='blue',
                subtitle=f"[blue]{v['links']['info']}",
                subtitle_align='right',
            )
        )

def clean_description(text: str) -> str:
    """Parse strain description html as text"""

    text = BeautifulSoup(text, 'html.parser').text.replace('<br />','\n').replace('&quot;','"').rstrip()
    return text

def rank_results(search_results: list[dict], search: str, key: str) -> list[dict]:
    return sorted(search_results, key=lambda z: SequenceMatcher(None, z[key], search).ratio(), reverse=True)

def parse() -> argparse.Namespace:
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(description='Search strain on seedfinder')
    parser.add_argument('query', nargs='+',
                        help='search query')
    parser.add_argument('-l', '--limit', nargs='?', type=int, default=5,
                        help='number of results to show. default is 5')
    parser.add_argument('-ni', '--not-interactive', action='store_false', default=True,
                        help='don\'t use interactive prompt. print first page of results and exit program')
    return parser.parse_args()

def main():
    args = parse()
    load_dotenv()
    api_key = os.getenv('SF_API_KEY')
    if api_key is None:
        help_url = 'https://en.seedfinder.eu/userarea/action/jsonapi.html'
        print(f'\n[red]No API key found.[/] Set the environment variable "SF_API_KEY" to your seedfinder.eu API key.\nSee {help_url} for more information\n')
        exit()
    sf = SeedFinder(api_key)
    query = ' '.join(args.query)
    interactive = args.not_interactive
    search(sf, query, limit=args.limit, print_results=True, interactive=interactive)

if __name__ == '__main__':
    main()