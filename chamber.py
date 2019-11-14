"""U.S. Chamber of Commerce parsing"""
import json
import datetime
import re
import requests
from bs4 import BeautifulSoup


# TODO: Improve parsing
# This parser is not perfect. Does not correctly handle multiline companies, e.g.
#
# Glenn Hamer
# President and
# Chief Executive Officer
# Arizona Chamber of Commerce
# and Industry
# Phoenix, AZ
#
# also does not correctly handle multiple listed affiliations, e.g.
#
# John Ruan III
# Executive Chairman
# Ruan Transportation
# Management Systems
# Chairman and CEO, BTC Financial Corporation
# Chairman and CEO, Ruan, Incorporated
# Des Moines, IA

def get_chamber_directors():
    """Scrapes US Chamber of Commerce for board of directors, writes chamber_directors.json file"""
    url = 'https://www.uschamber.com/about/board-of-directors'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    city_re = re.compile('(.*, ([A-Z]{2}|Canada)|Bermuda)')
    directors = list()
    for director in soup.select("table p"):
        if not director.find("strong"):
            continue
        director_dict = {
            'name' : director.find("strong").text
        }
        if len(director.contents) >= 3:
            last_line = director.contents[-1:][0]
            if city_re.match(last_line):
                director_dict['city'] = last_line
            else:
                director.append(soup.br) # add dummy line for missing city
                director.append(' ')
        if len(director.contents) >= 5:
            director_dict['company'] = director.contents[-3:-2][0]
        if len(director.contents) >= 7:
            title = " ".join([s for s in director.contents[2:-4] if isinstance(s, str)])
            director_dict['title'] = title
        directors.append(director_dict)
    directors_dict = {
        'retrieved_at' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'directors' : directors
        }
    with open('chamber_directors.json', 'w', encoding='utf-8') as json_f:
        json.dump(directors_dict, json_f, ensure_ascii=False, indent=4)
    return directors
