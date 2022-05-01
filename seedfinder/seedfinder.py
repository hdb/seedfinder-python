#! /bin/env python3

import requests

class SeedFinder:
    """API client object to authorize and perform seedfinder.eu query requests"""

    def __init__(self, api_key=None):

        base_url = 'https://en.seedfinder.eu/api/json/'

        self.search_api = base_url + 'search.json'
        self.breeders_api = base_url + 'ids.json'
        self.strain_api = base_url + 'strain.json'
        self.thread_api = base_url + 'threadfinder.json'

        self.api_auth = '&ac={}'.format(api_key) if api_key is not None else ''

    def searchStrain(self, strain, exact=False):
        """Search for strain names and return basic strain information. Use exact flag to only return exact matches.
        
        https://en.seedfinder.eu/api/json/search/
        """

        strain_str = strain.replace('#','%23')
        url = '{}?q={}'.format(self.search_api, strain_str)
        results = self._get(url)
        if exact and not results['error'] and results['count']>0:
            results['strains'] = {k:v for k,v in results['strains'].items() if v['name'] == strain or v['id'] == strain}
            matches = len(results['strains'])
            if matches == 0:
                results['info'] = 'Sorry, nothing was found for your search.'
                del results['strains']
            else:
                results['info'] = results['info'].replace(str(results['count']), str(matches))
            results['count'] = matches
        return results

    def strainInfo(self, strain_id, breeder_id='Unknown_or_Legendary', lang='en', show_parents=False, show_hybrids=False, show_med_info=False, show_pics=False, comments=0, forums=[], show_reviews=False, show_tasting=False, hide_taste= False, hide_smell=False, hide_effect=False):
        """Get detailed information for a given strain. Requires seedfinder strain id and the strain's breeder id.
        
        https://en.seedfinder.eu/api/json/strain/
        """

        parents = '1' if show_parents else '0'
        hybrids = '1' if show_hybrids else '0'
        med_info = '1' if show_med_info else '0'
        pics = '1' if show_pics else '0'
        forums_str = '' if len(forums) < 1 else '&forums={}'.format('|'.join(forums))

        reviews = '1' if show_reviews else '0'
        smell = '0' if hide_smell else '1'
        taste = '0' if hide_taste else '1'
        effect = '0' if hide_effect else '1'
        tasting_str = '&tasting=1&smell={}&taste={}&effect={}'.format(smell, taste, effect) if show_tasting and show_reviews else ''

        url = '{}?br={}&str={}&lng={}&parents={}&hybrids={}&medical={}&pics={}&comments={}&commlng={}{}&reviews={}{}'.format(
            self.strain_api, breeder_id, strain_id, lang, parents, hybrids, med_info, pics, comments, lang, forums_str, reviews, tasting_str
        )

        return self._get(url)

    def parents(self, strain_id, breeder_id='Unknown_or_Legendary', generations=1):
        """Get parent strains of a given strain. Requires seedfinder strain id and the strain's breeder id.
        
        https://en.seedfinder.eu/api/json/strain/
        """

        strain_info = self.strainInfo(strain_id, breeder_id, show_parents=True)
        parents = strain_info['parents']
        parents['child'] = {
            'name': strain_info['name'],
            'id': strain_id,
            'brname': strain_info['brinfo']['name'],
            'brid': breeder_id
        }
        elders = []
        if generations > 1:
            for k,v in parents['strains'].items():
                if v['id'] != 'Indica' and v['id'] != 'Sativa' and v['brid'] != 'Original_Strains':
                    elders = elders + self.parents(v['id'],v['brid'],generations=generations-1)

        return [parents] + elders

    def hybrids(self, strain_id, breeder_id='Unknown_or_Legendary', generations=1):
        """Get hybrids of a given strain. Requires seedfinder strain id and the strain's breeder id.
        
        https://en.seedfinder.eu/api/json/strain/
        """

        strain_info = self.strainInfo(strain_id, breeder_id, show_hybrids=True)
        hybrids = strain_info['hybrids']
        if hybrids == False:
            return []
        progeny = []
        if generations > 1:
            for k,v in hybrids.items():
                progeny = progeny + self.hybrids(v['id'],v['brid'],generations=generations-1)
        hybrids['parent'] = {
            'name': strain_info['name'],
            'id': strain_id,
            'brname': strain_info['brinfo']['name'],
            'brid': breeder_id
        }
        return [hybrids] + progeny

    def breederInfo(self, breeder_id, show_strains=True):
        """Get all strains developed by a given breeder.
        
        https://en.seedfinder.eu/api/json/ids/
        """

        strains = '1' if show_strains else '0'
        url = '{}?br={}&strains={}'.format(self.breeders_api, breeder_id, strains)
        return self._get(url)

    def thread(self, forum, thread):
        """Get all strains for the selected thread and connected threads
        
        https://en.seedfinder.eu/api/json/threadfinder/
        """

        thread = str(thread)
        url = '{}?forum={}&thread={}'.format(self.thread_api, forum, thread)
        return self._get(url)

    def _get(self, url):
        url += self.api_auth
        response = requests.get(url)
        data = response.json()
        return data
