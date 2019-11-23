"""U.S. Chamber of Commerce parsing"""
import re
from scraper import Scraper

# TODO: Improve parsing
# This parser is not perfect. Does not correctly handle multiple listed affiliations, e.g.
#
# John Ruan III
# Executive Chairman
# Ruan Transportation
# Management Systems
# Chairman and CEO, BTC Financial Corporation
# Chairman and CEO, Ruan, Incorporated
# Des Moines, IA

class Chamber(Scraper):
    """U.S. Chamber of Commerce scraper"""
    def __init__(self):
        super().__init__()
        self.url = 'https://www.uschamber.com/about/board-of-directors'
        self.name = 'U.S. Chamber of Commerce'
        self.relationship = 'director'
        self.soup = self.get_soup(self.url)

def get_people(self):
    """Scrapes US Chamber of Commerce for board of directors"""
    city_re = re.compile('(.*,? ([A-Z]{2}|Canada)|Bermuda)')
    directors = list()
    for director in self.soup.select("table p"):
        if not director.find("strong"):
            continue
        director_dict = { # name is the only standard-formatted element
            'name' : director.find("strong").text
        }
        if len(director.contents) >= 3:  # parse city
            last_line = director.contents[-1]
            if city_re.match(last_line):
                director_dict['city'] = last_line
            else:
                director.append(soup.br) # add dummy line for missing city
                director.append(' ')
        if len(director.contents) >= 5: # parse company
            company = director.contents[-3]
            extra = []
            while re.match('^Chairman.*', company): # secondary affiliations
                title, co = re.match('(^Chairman[^,]+), (.*)', company).group(1, 2)
                extra.append({'title' : title, 'company' : co})
                director.contents.pop(-3)
                director.contents.pop(-2)
                company = director.contents[-3]
            if extra:
                director_dict['extra_affiliations'] = extra
            if re.match('[a-z]', company): # if multiline company
                company = director.contents.pop(-5) + " " + company
                director.contents.pop(-4) # pop the br tag
            director_dict['company'] = company
        if len(director.contents) >= 7: # parse title
            title = " ".join([s for s in director.contents[2:-4] if s.string])
            director_dict['title'] = title
        directors.append(director_dict)
    return directors
