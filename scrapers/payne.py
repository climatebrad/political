"""payne.py
Payne Institute scraper"""
from scraper import Scraper

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

    def get_person_dict(self, person):
        person_dict = { # name is the only standard-formatted element
            'name' : person.find("h4").text,
            'blurb' : person.find("p").text,
            'bio' : self.get_payne_director_bio(person.find("a")['href'])
        }
        return person_dict

    def get_people(self):
        people = list()
        for person in self.soup.select(".et_pb_text_inner"):
            if not person.find("h4"):
                continue
            people.append(self.get_person_dict(person))
        return people
