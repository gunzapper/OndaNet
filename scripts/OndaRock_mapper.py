"""
To reach only the needed information from an OndaRock Page
using a pratical class
"""

__author__ = 'Pietro Brunetti aka gunzapper'

import re
# a list of patterns

album_pattern = re.compile(r'^/(recensioni)/(\d{4})_(\w+)\.htm$')
pietre_miliari_pattern = re.compile(r'^/(pietremiliari)/(\w+)\.htm$')
artist_pattern = re.compile(r'^/(rockedintorni|popmuzik|dark|songwriter|altrisuoni|italia|jazz|interviste)/(\w+)\.htm$')
gender_pattern = re.compile(r'^/(storiadelrock)/(\w+)\.htm$')

general_pattern = re.compile('^/\w+/\w+\.htm$')

root_pattern = re.compile('^(http|https)://www\.\w+\.\w+')

import requests
from bs4 import BeautifulSoup

class OndaRock_mapper_error(Exception):
    pass

class General_parser_error(OndaRock_mapper_error):
    pass

class Album_Error(OndaRock_mapper_error):
    pass

class General_parser(object):
    def __init__(self, root, path):
        m1 = root_pattern.match(root)
        m2 = general_pattern.match(path)
        if  m1 and m2:
            self.root = root
            self.path = path
        else:
            msg = "the url {0}{1} does not smell as a valid url"
            raise General_parser_error, msg.format(root, path)

    def get_soup(self):
        """
        for BeautifulSoup works

        :param self:
        :return: BeautifulSoup parser
        :rtype: BeautifulSoup
        """

        r = requests.get(self.get_url())
        assert(r.status_code == 200)

        return(BeautifulSoup(r.text))

    def iter_links(self):
        """
        Starting from a web page
        iter_links iterates for each anchor in the page

        :param self:
        """
        for anchor in self.get_soup().findAll('a'):
            link = anchor.get('href')
            m = general_pattern.match(link)
            if m:
                yield link

    def get_url(self):
        return "".join([self.root, self.path])

class Album_parser(General_parser):
    def __init__(self, root, path):
        General_parser.__init__(self, root, path)
        s = album_pattern.search(path)
        if not s:
            raise Album_Error, "The url {0} don't look as an album".format(path)
        try:
            soup = self.get_soup()
        except AssertionError:
            raise Album_Error, "Page {0}{1} no found".format(self.root, self.path)
        else:
            self.artist = soup.body.h1.text
            self.title = soup.body.h2.text
            dati = soup.body.div(id="dati")[0].text
            # for example u'2010 (Bela Union) | folk-rock'
            self.year = dati[0:4]
            op_br = dati.find('(')+1
            cl_br = dati.find(')')
            self.label = dati[op_br:cl_br]
            self.genders = dati[cl_br+3:].split(',')

    def __repr__(self):
        return "<OndaRockAlbum_parser of {0}>".format(self.path)



if __name__ == "__main__":

    root = 'http://www.ondarock.it'
    example = Album_parser(root, "/recensioni/2014_temples_sunstructures.htm")
    print(example.artist)
    print(example.title)
    print(example.genders)
    print(example.year)
    print(example.label)

    for link in example.iter_links():
        print(link)

    print example.get_url()

