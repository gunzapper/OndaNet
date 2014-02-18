"""
To reach only the needed information from an OndaRock Page
using a pratical class
"""

__author__ = 'Pietro Brunetti aka gunzapper'

import requests
from bs4 import BeautifulSoup

class OndaRockAlbum_parser:
    def __init__(self, url):
        self.url = url
        soup = self.__get_soup()
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

        :param url: the url of a web page
        :type url: str
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

        :param soup: the parser for the page
        :type url: BeautifulSoup
        :param root: the page 'home'
        :type root: str
        """
        for anchor in self.__get_soup().findAll('a'):
            link = anchor.get('href')
            yield link

if __name__ == "__main__":
    example = OndaRockPage_parser("http://www.ondarock.it/recensioni/2010_midlake.htm")
    print(example.artist)
    print(example.title)
    print(example.genders)
    print(example.year)
    print(example.label)



