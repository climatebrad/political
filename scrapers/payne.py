"""payne.py
Payne Institute scraper"""
import requests
from scraper import Scraper
from bs4 import BeautifulSoup

class Payne(Scraper):
    def __init__(self):
        super().__init__()
        self.url = 'https://payneinstitute.mines.edu/advisory-board/'
        self.name = 'Payne Institute for Public Policy'
        self.relationship = 'advisory board member'
        self.soup = self.get_soup(self.url)

    def get_payne_director_bio(self, url):
        soup = self.get_soup(url)
        bio = soup.select_one(".et_pb_text_inner")
        for strong_tag in bio.find_all('strong'):
            strong_tag.decompose()
        return bio.text

    def get_people(self):
        people = list()
        for person in self.soup.select(".et_pb_text_inner"):
            if not person.find("h4"):
                continue
            person_dict = { # name is the only standard-formatted element
                'name' : person.find("h4").text,
                'blurb' : person.find("p").text,
                'bio' : self.get_payne_director_bio(person.find("a")['href'])
            }
            people.append(person_dict)
        return people
