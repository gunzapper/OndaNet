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
from networkx.readwrite import json_graph
import http_server
import json

import OndaRock_mapper as mapper

# a list of patterns
album_pattern = re.compile(r'(^/recensioni/)(?P<year>\d{4})_(?P<band>\w+)_(?P<album>\w+)\.htm$')
pietre_miliari_pattern = re.compile(r'(^/pietremiliari/)(?P<band>\w+)_(?P<album>\w+)\.htm$')
artist_pattern = re.compile(r'(?<=^/)(\w+)/(\w+)(?=\.htm$)')
gender_pattern = re.compile(r'(^/storiadelrock/)(?P<gender>w+)\.htm$')

# general pattern valid for each ondarock anchor
general_pattern = re.compile(r"(?<=^/)(\w+)/(\w+)(?=\.htm$)")

def get_soup(url):
    """
   for BeautifulSoup works

    :param url: the url of a web page
    :type url: str
    :return: BeautifulSoup parser
    :rtype: BeautifulSoup
    """

    r = requests.get(url)
    assert(r.status_code == 200)

    return(BeautifulSoup(r.text))

def iter_links(soup):
    """
    Starting from a web page
    iter_links iterates for each anchor in the page

    :param soup: the parser for the page
    :type url: BeautifulSoup
    :param root: the page 'home'
    :type root: str
    """

    for anchor in soup.findAll('a'):
        link = anchor.get('href')
        yield link

def album_name(soup):
    """
    From the album name return the album name
    Used as label of the corresponding node

    :param soup: the parser for the page
    :type url: BeautifulSoup
    """
    entire_title = soup.title.string
    cut_off = entire_title.find('::')
    title = entire_title[:cut_off]
    title = re.subn(' - ', '\n', title, 1)[0]
    # probably faster but deprecated
    #title.replace(' - ', '\n', 1)
    return title

def only_album(url, ondagraph, root="http://www.ondarock.it"):
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
    :param root: the home portal
    :type root: str
    :return: the Node Name
    :rtype: str
    """

    entire_url = ''.join([root, url])
    try:
        soup = get_soup(entire_url)
    # If iter_links does not open the page
    except AssertionError:
        print("Impossible to reach {0}".format(link))
        print("It will not be added to the graph\nsorry.")
    else:
        nodeName = album_name(soup)
        ondagraph.add_node(url, group=0)
        for link in iter_links(soup):
            if album_pattern.match(link):
                # less parsing solution
                linkName = only_album(link, ondagraph)

                # less memory solution
                #linksoup = get_soup(''.join([root, link]))
                #linkName = album_name(linksoup)
                #only_album(link, ondagraph)

                # TODO: not recursive solution
                ondagraph.add_edge(url, link)

        return nodeName

def serialize(graph, file="force/force.json"):
    """
    Write the graph in the force json file

    :param graph: NetworkX graph
    :param file: output json file
    """
    d = json_graph.node_link_data(graph) # node-link format to serialize
    json.dump(d, open('force/force.json','w'), indent=4)

def album_net(album_link):
    """
    Return the album net -
    The network that describes
    How many other album are connected
    to this one.
    It's a simple facade.

    >>>album_net(r"/recensioni/2014_aavv_sullagiostranellombra.htm")

    :param album_net: the inner url of ondarock page
    :type url: str
    :return: the album graph
    :rtype: networkx.Graph
    """
    # initialize a directional graph
    ondaGraph = nx.DiGraph()
    # initialize a graph
    #ondaGraph = nx.Graph()
    # populating the graph
    only_album(album_link, ondaGraph)

    return(ondaGraph)


if __name__ == "__main__":
    # examples
    #url = r"/recensioni/2014_aavv_sullagiostranellombra.htm"
    #url = r"/recensioni/2012_prostitutes_psychedelicblack.htm"
    url = r'/recensioni/2014_sunkilmoon_benji.htm'

    a_n = album_net(url)
    serialize(a_n)
    http_server.load_url('force/force.html')
