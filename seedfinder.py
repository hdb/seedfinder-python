#! /bin/env python3

import requests

class SeedFinder:

    def __init__(self, api_key):

        base_url = 'https://en.seedfinder.eu/api/json/'

        self.search_api = base_url + 'search.json'
        self.breeders_api = base_url + 'ids.json'
        self.strain_api = base_url + 'strain.json'
        self.thread_api = base_url + 'threadfinder.json'

        self.api_auth = '&ac={}'.format(api_key)

    def searchStrain(self, strain):
        strain_str = strain.replace('#','%23')
        url = '{}?q={}'.format(self.search_api, strain_str)
        return self.get(url)

    def strain_info(self, strain_id, breeder_id='Unknown_or_Legendary', lang='en', show_parents=False, show_hybrids=False, show_med_info=False, show_pics=False, comments=0, forums=[], show_reviews=False, show_tasting=False, hide_taste= False, hide_smell=False, hide_effect=False):
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

        return self.get(url)

    def parents(self, strain_id, breeder_id='Unknown_or_Legendary'):
        strain_info = self.strain_info(strain_id, breeder_id, show_parents=True)
        return strain_info['parents']

    def hybrids(self, strain_id, breeder_id='Unknown_or_Legendary'):
        strain_info = self.strain_info(strain_id, breeder_id, show_hybrids=True)
        return strain_info['hybrids']

    def breeder_info(self, breeder_id, show_strains=False):
        strains = '1' if show_strains else '0'
        url = '{}?br={}&strains={}'.format(self.breeders_api, breeder_id)
        return self.get(url)

    def thread(self, forum, thread):
        thread = str(thread)
        url = '{}?forum={}&thread={}'.format(self.thread_api, forum, thread)
        return self.get(url)

    def get(self, url):
        url += self.api_auth
        response = requests.get(url)
        data = response.json()
        return data

def main():
    pass

if __name__ == "__main__":
    main()