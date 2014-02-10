__author__ = 'Pietro Brunetti aka gunzapper'

import requests
import networkx as nx
import BeautifulSoup as bs
import re

album_pattern = re.compile(r'/recensioni/(?P<year>\d{4})_(?P<band>\w+)_(?P<album>\w+)\.htm')

def iter_links(url, root="http://www.ondarock.it/"):
    r = requests.get(''.join([root, url]))
    assert(r.status_code == 200)

    soup = bs.BeautifulSoup(r.text)

    for anchor in soup.findAll('a'):
        link = anchor.get('href')
        if album_pattern.match(link):
            yield link

def album_name(url):
    pieces = url.split('_')
    return "%s-%s" %(pieces[1], pieces[2][:-4])


def record_ondagraph(url, ondagraph):
    nodeName = album_name(url)
    ondagraph.add_node(nodeName)

    for link in iter_links(url):
        linkName = album_name(link)
        ondagraph.add_edge(nodeName, linkName)
        print link
        record_ondagraph(link, ondagraph)


if __name__ == "__main__":
    url = r"recensioni/2014_aavv_sullagiostranellombra.htm"
    #url = r"/recensioni/2012_prostitutes_psychedelicblack.htm"

    ondaGraph = nx.Graph()
    record_ondagraph(url, ondaGraph)

    print ondaGraph.nodes()

    import matplotlib.pyplot as plt
    nx.draw(ondaGraph)
    plt.show()