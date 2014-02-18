"""
To reach only the needed information from an OndaRock Page
using a pratical class
"""

__author__ = 'Pietro Brunetti aka gunzapper'

import re
# a list of patterns
#root_pattern = re.compile('^http://www\.ondarock\.it')
album_pattern = re.compile(r'(recensioni)/(\d{4})_(\w+)\.htm$')
pietre_miliari_pattern = re.compile(r'(pietremiliari)/(\w+)\.htm$')
artist_pattern = re.compile(r'(rockedintorni|popmuzik|dark|songwriter|altrisuoni|italia|jazz)/(\w+)\.htm$')
gender_pattern = re.compile(r'(storiadelrock)/(\w+)\.htm$')

general_pattern = re.compile('/\w+/\w+\.htm$')

root = 'http://www.ondarock.it'

import requests
from bs4 import BeautifulSoup

class OndaRock_mapper_error(Exception):
    pass

class General_parser_error(OndaRock_mapper_error):
    pass

class Album_Error(OndaRock_mapper_error):
    pass

class General_parser(object):
    def __init__(self, url):
        if url.find(root) == 0:
            self.url = url
        else:
            m = general_pattern.search(url)
            if m:
                self.url = ''.join([root, url])
            else:
                raise General_parser_error, "the url {0} does not smell as a url"

    def get_soup(self):
        """
        for BeautifulSoup works

        :param self:
        :return: BeautifulSoup parser
        :rtype: BeautifulSoup
        """

        r = requests.get(self.url)
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
            yield link

class Album_parser(General_parser):
    def __init__(self, url):
        General_parser.__init__(self, url)
        s = album_pattern.search(url)
        if not s:
            raise Album_Error, "The url {0} does not match the right pattern".format(url)
        try:
            soup = super(Album_parser, self).get_soup()
        except AssertionError:
            raise Album_Error, "Page {0} no found".format(self.url)
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
        return "<OndaRockAlbum_parser of {0}>".format(url)



if __name__ == "__main__":
    example = Album_parser("http://www.ondarock.it/recensioni/2010_midlake.htm")
    print(example.artist)
    print(example.title)
    print(example.genders)
    print(example.year)
    print(example.label)

    for link in example.iter_links():
        print(link)

    print example.url

    example2 = Album_parser("/recensioni/2010_midlake.htm")
    print example2.url


