#!/usr/bin/python3 -OO

import json
from urllib.request import urlopen


def get_links(name, plcontinue=False):
    url = 'https://en.wikipedia.org/w/api.php?action=query&format=json&prop=links&pllimit=500&plnamespace=0&titles=%s' % name
    # if more than 500 results were returned, get the rest of them.
    if plcontinue:
        url += '&plcontinue=%s' % plcontinue
    data = json.loads(urlopen(url).read().decode())
    # we don't have the pageid, so we just pop the first page from pages.
    pagelist = data['query']['pages'].popitem()[1]['links']
    links = [page['title'] for page in pagelist]
    if 'query-continue' in data:
        links += get_links(name, data['query-continue']['links']['plcontinue'])
    return links


def main():
    print(get_links("Albert_Einstein"))
    print(get_links("Fox"))

if __name__ == "__main__":
        main()
