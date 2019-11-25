"""org-people scraper"""
import json
import datetime
import re
import requests
from scrapers.payne import Payne
from scrapers.chamber import Chamber

def get_org_people(scraper):
    org_scraper = scrapers[scraper]
    org_people_dict = {
        'retrieved_at' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'organization' : org_scraper.name,
        'default_relationship' : org_scraper.relationship,
        'people' : org_scraper.get_people()
    }
    return org_people_dict
#     ".et_pb_text_inner h4 a"

def save_org_people(org_name, people_dict):
    """write dict to json file with org_name"""
    filename = org_name.lower().replace(" ","_")
    with open(f'{filename}.json', 'w', encoding='utf-8') as json_f:
        json.dump(people_dict, json_f, ensure_ascii=False, indent=4)

payne = Payne()
paynefellows = Payne('fellows')
scrapers = {}
scrapers[payne.name] = payne
scrapers['paynefellows'] = paynefellows

for scraper in scrapers:
    people = get_org_people(scraper)
    print(people)
    save_org_people(scraper, people)


# get_bio('https://payneinstitute.mines.edu/project/nawal-al-hosany/')
