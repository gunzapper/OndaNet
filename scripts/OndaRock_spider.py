"""
A first script to collected the network between
pages in OndaRock portal

This script collects all albums linked to a first one
"""

__author__ = 'Pietro Brunetti aka gunzapper'

import requests
import networkx as nx
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt

# a list of patterns
album_pattern = re.compile(r'(^/recensioni/)(?P<year>\d{4})_(?P<band>\w+)_(?P<album>\w+)\.htm$')
#group_pattern = re.compile(r'(?<=^/)(\w+)/(\w+)(?=\.htm$)')
#gender_pattern = re.compile(r'(^/storiadelrock/)(?P<gender>w+)\.htm$')

# general pattern valid for each ondarock anchor
#general_pattern = re.compile(r"(?<=^/)(\w+)/(\w+)(?=\.htm$)")


def iter_links(url, root="http://www.ondarock.it/"):
    """
    Starting from a web page
    iter_links iterates for each anchor in the page

    >>>for link in iter_links(r"/recensioni/2014_aavv_sullagiostranellombra.htm")):
    ...    print(link)

    :param url: the url of ondarock page
    :type url: str
    :param root: the page 'home'
    :type root: str
    """
    r = requests.get(''.join([root, url]))
    assert(r.status_code == 200)

    soup = BeautifulSoup(r.text)

    for anchor in soup.findAll('a'):
        link = anchor.get('href')
        yield link

def album_name(url):
    """
    From the album name return the album name
    Used as label of the corresponding node

    >>>album_name(r"/recensioni/2014_aavv_sullagiostranellombra.htm")
    aavv
    sullagiostranellombra

    :param url: the url of ondarock page
    :type url: str
    """
    pieces = url.split('_')
    return "%s\n%s" %(pieces[1], pieces[2][:-4])


def only_album(url, ondagraph):
    """
    Recursive function that populates the graph
    of nodes and edges regarding only album web pages

    >>>import networkx as nx
    >>>ondaGraph = nx.Graph()
    >>>only_album(r'/recensioni/2014_sunkilmoon_benji.htm', ondaGraph)

    :param url: the url of ondarock page
    :type url: str
    :param ondagraph: the graph
    :type ondagraph: networkx.Graph
    """
    nodeName = album_name(url)
    ondagraph.add_node(nodeName)
    print("{0} is linked to:".format(nodeName))
    try:
        for link in iter_links(url):
            if album_pattern.match(link):
                linkName = album_name(link)
                print("\t{0}\n".format(linkName))

                ondagraph.add_edge(nodeName, linkName)
                only_album(link, ondagraph)

    # If iter_links does not open the page
    except AssertionError:
        print("Impossible to reach {0}".format(link))
        print("It will not be added to the graph\nsorry.")


def album_net(album_link, plot=True):
    """
    Return the album net -
    The network that describes
    How many other album are connected
    to this one.
    It's a simple facade.

    >>>album_net(r"/recensioni/2014_aavv_sullagiostranellombra.htm")

    :album_net: the inner url of ondarock page
    :type url: str
    :param plot: Do you need to see the graph plot?
    :type ondagraph: bool
    :return: the album graph
    :rtype: networkx.Graph
    """
    # initialize a graph
    ondaGraph = nx.Graph()
    # populating the graph
    only_album(album_link, ondaGraph)

    if plot:
        # plot the graph
        nx.draw(ondaGraph)
        plt.show()
    return(ondaGraph)


if __name__ == "__main__":
    # examples
    #url = r"/recensioni/2014_aavv_sullagiostranellombra.htm"
    #url = r"/recensioni/2012_prostitutes_psychedelicblack.htm"
    url = r'/recensioni/2014_sunkilmoon_benji.htm'

    a_n = album_net(url)