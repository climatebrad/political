"""payne.py
Payne Institute scraper"""
from scraper import Scraper

class Payne(Scraper):
    def __init__(self, page='board'):
        super().__init__()
        self.pages = {
            'board' : {
                'url' : 'https://payneinstitute.mines.edu/advisory-board/',
                'relationship' : 'advisory board member'
            },
            'fellows' : {
                'url' : 'https://payneinstitute.mines.edu/fellows/',
                'relationship' : 'fellow'
            }
        }
        self.url = self.pages[page]['url']
        self.name = 'Payne Institute for Public Policy'
        self.relationship = self.pages[page]['relationship']
        self.soup = self.get_soup(self.url)

    def get_payne_bio(self, url):
        soup = self.get_soup(url)
        bio_text = None
        if 'mines.edu' in url: # on the payne website:
            bio = soup.select_one(".et_pb_text_inner")
            for strong_tag in bio.find_all('strong'):
                strong_tag.decompose()
            bio_text = bio.text
        elif 'academia.edu' in url:
            bio_text = soup.select_one(".js-profile-about").text
        return bio_text

    def get_person_blurb(self, person):
        tags = person_text.find_all(["p", "div"])
        return " ".join([tag.get_text(separator=' ') for tag in tags])

    def get_person_dict(self, person):
        person_text = person.select_one(".et_pb_text_inner")
        person_dict = {
            'name' : person_text.find("h4").text,
            'blurb' : self.get_person_blurb(person),
            'bio' : self.get_payne_bio(person.find("a")['href']),
            'image_url' : person.find("img")['src'],
        }
        return person_dict


    def get_people(self):
        people = list()
        for person in self.soup.select(".et_pb_column.et_pb_column_1_4"):
            if not person.find("h4"):
                continue
            people.append(self.get_person_dict(person))
        return people
