#!/usr/bin/python3 -OO

import json
from urllib.request import urlopen
from urllib.parse import quote


class Node():
    def __init__(self, name, cost=1, parent=None):
        self.name = name
        self.cost = cost
        self.parent = parent

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name


def get_links(node, plcontinue=False):
    print(node)
    url = 'http://en.wikipedia.org/w/api.php?action=query&format=json&prop=links&pllimit=500&plnamespace=0&titles=%s' % quote(str(node))
    # if more than 500 results were returned, get the rest of them.
    if plcontinue:
        url += '&plcontinue=%s' % quote(plcontinue)
    data = json.loads(urlopen(url).read().decode())
    # we don't have the pageid, so we just pop the first page from pages.
    pagelist = data['query']['pages'].popitem()[1]
    if 'links' in pagelist:
        pagelist = pagelist['links']
    else:
        return []
    links = [page['title'] for page in pagelist]
    if 'query-continue' in data:
        pass
        #links += get_links(node, data['query-continue']['links']['plcontinue'])
    if plcontinue:
        return links
    else:
        return [Node(link, node.cost+1, node) for link in links]


def get_path(node):
    path = []
    while node.parent:
        path.append(str(node))
        node = node.parent
    path.append(str(node))
    return " -> ".join(reversed(path))


def find_path(start, end):
    closedlist = []
    openlist = [start]
    while openlist:
        current = min(openlist, key=lambda link: link.cost)
        if current == end:
            return get_path(current)
        openlist.remove(current)
        closedlist.append(current)
        for link in get_links(current):
            if link not in closedlist:
                if link not in openlist:
                    openlist.append(link)


def main():
    start = Node("Fox")
    end = Node("Cat")
    path = find_path(start, end)
    print(path)

if __name__ == "__main__":
        main()
