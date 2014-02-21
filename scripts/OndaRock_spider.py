"""
A first script to collected the network between
pages in OndaRock portal

This script collects all albums linked to a first one
"""

__author__ = 'Pietro Brunetti aka gunzapper'

import networkx as nx

from networkx.readwrite import json_graph
import json

import OndaRock_mapper as mapper


def only_album(url, ondagraph, group, root="http://www.ondarock.it"):
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
    """
    print url
    album = mapper.Album_parser(root, url)
    # yeah, I could do a serialization using Monkey-Patch DP
    # but explicit is better than implicit #Python #ZEN
    ondagraph.add_node(url, group=group,
                       title=album.title,
                       artist=album.artist,
                       genders = album.genders,
                       label=album.label,
                       rate=album.rate,
                       year=album.year)
    for link in album.iter_links():
        m = mapper.album_pattern.match(link)
        if m:
            print '\t', link
            ondagraph.add_edge(url, link)
    for link in album.iter_links():
        m = mapper.album_pattern.match(link)
        # recourse only for new link - not lost in loops
        if m and not ondagraph[link].has_key("title"):
            only_album(link, ondagraph, 1)

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
    #ondaGraph = nx.DiGraph()
    # initialize a graph
    ondaGraph = nx.Graph()
    # populating the graph
    only_album(album_link, ondaGraph, 0)

    return(ondaGraph)


if __name__ == "__main__":
    # examples
    url = r"/recensioni/2014_aavv_sullagiostranellombra.htm"
    #url = r'/recensioni/2014_sunkilmoon_benji.htm'

    a_n = album_net(url)
    serialize(a_n)

