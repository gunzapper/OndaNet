__author__ = 'Pietro Brunetti aka gunzapper'

import requests
import networkx as nx
from bs4 import BeautifulSoup
import re

album_pattern = re.compile(r'(^/recensioni/)(?P<year>\d{4})_(?P<band>\w+)_(?P<album>\w+)\.htm$')
group_pattern = re.compile(r'(?<=^/)(\w+)/(\w+)(?=\.htm$)')
gender_pattern = re.compile(r'(^/storiadelrock/)(?P<gender>w+)\.htm$')

general_pattern = re.compile(r"(?<=^/)(\w+)/(\w+)(?=\.htm$)")

#chose the type reading the html

def iter_links(url, root="http://www.ondarock.it/"):
    r = requests.get(''.join([root, url]))
    assert(r.status_code == 200)

    soup = BeautifulSoup(r.text)

    for anchor in soup.findAll('a'):
        link = anchor.get('href')
        yield link

def album_name(url):
    pieces = url.split('_')
    return "%s\n%s" %(pieces[1], pieces[2][:-4])

def only_album(url, ondagraph):
    nodeName = album_name(url)
    ondagraph.add_node(nodeName)

    for link in iter_links(url):
        if album_pattern.match(link):
            linkName = album_name(link)
            ondagraph.add_edge(nodeName, linkName)
            only_album(link, ondagraph)
        #elif group_pattern.match(link): print link
        else: print link

if __name__ == "__main__":
    url = r"/recensioni/2014_aavv_sullagiostranellombra.htm"
    #url = r"/recensioni/2012_prostitutes_psychedelicblack.htm"

    ondaGraph = nx.Graph()
    only_album(url, ondaGraph)

    import matplotlib.pyplot as plt
    nx.draw(ondaGraph)
    plt.show()