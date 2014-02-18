"""
To reach only the needed information from an OndaRock Page
using a pratical class
"""

__author__ = 'Pietro Brunetti aka gunzapper'

import re
# a list of patterns
album_pattern = re.compile(r'(recensioni)/(\d{4})_(\w+)\.htm$')
pietre_miliari_pattern = re.compile(r'(pietremiliari)/(\w+)\.htm$')
artist_pattern = re.compile(r'(rockedintorni|popmuzik|dark|songwriter|altrisuoni|italia|jazz)/(\w+)\.htm$')
gender_pattern = re.compile(r'(storiadelrock)/(\w+)\.htm$')

import requests
from bs4 import BeautifulSoup

class OndaRock_mapper_error(Exception):
    pass

class OndaRockAlbum_Error(OndaRock_mapper_error):
    pass

class OndaRockAlbum_parser:
    def __init__(self, url):
        s = album_pattern.search(url)
        if not s:
            raise OndaRockAlbum_Error, "The url {0} does not match the right pattern".format(url)
        self.url = url
        try:
            soup = self.__get_soup()
        except AssertionError:
            print("Page {0} no found".format(self.url))
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
        return "<OndaRockPage_parser of {0}>".format(url)

    def __get_soup(self):
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
        for anchor in self.__get_soup().findAll('a'):
            link = anchor.get('href')
            yield link

if __name__ == "__main__":
    example = OndaRockAlbum_parser("http://www.ondarock.it/recensioni/2010_midlake.htm")
    print(example.artist)
    print(example.title)
    print(example.genders)
    print(example.year)
    print(example.label)



