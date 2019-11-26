"""ipcc scraper"""
import re
from scraper import Scraper

class IPCC(Scraper):
    def __init__(self):
        super().__init__()
        self.reports_filename = 'ipcc_report_list'
        self.reports = []

    def get_report_ids(self):
        """load report_ids from site."""
        url = 'https://apps.ipcc.ch/report/authors/'
        return {int(option['value']) : option.text for option in
                self.get_soup(url).select('#cmbreport option') if option['value']}

    def get_report_chapter_ids(self, report_id):
        """gets json in format: [ { 'id' : #, 'description' : '..', .. """
        url = 'https://apps.ipcc.ch/report/authors/json/json.chapters.php?q=' + str(report_id)
        return [ { 'id' : x['id'],
                   'description' : x['description'],
                   'authors' : self.get_report_chapter_authors(report_id, x['id'])
                  } for x in self.get_json(url) ]

    def get_reports(self):
        """gets reports with chapters as json-style list"""
        return [ {'id' : id_,
                  'name' : name,
                  'chapters' : self.get_report_chapter_ids(id_)
                 } for id_, name in self.get_report_ids().items() ]

    def get_report_chapter_authors(self, report_id, chapter_id):
        """Gets report chapter authors. Combines results of two different pages."""
        authors_1 = self.get_report_chapter_authors_one(report_id, chapter_id)
        authors_2 = self.get_report_chapter_authors_two(report_id, chapter_id)
        for ix, author in enumerate(authors_1):
            author['person']['id'] = authors_2[ix]['person']['id']
            author['person']['photo'] = authors_2[ix]['person']['photo']
        return authors_1

    def get_report_chapter_authors_one(self, report_id, chapter_id):
        """Gets report chapter authors. Gets gender and citizenship, but not photo and id."""
        params = f'q={report_id}&p={chapter_id}'
        url = f'https://apps.ipcc.ch/report/authors/report.authors.php?{params}'
        authors = self.get_table(url)
        if authors: # there may not be any authors
            for ix, author in enumerate(authors):
                person = self.lowercase_keys(author)
                person['last name'] = person['last name'].title()
                authors[ix] = {
                    'index' : int(person.pop('unnamed: 0', None)) - 1,
                    'role' : person.pop('role', None),
                    'person' : person
                }
        else:
            authors = []
        return authors

    def get_report_chapter_authors_two(self, report_id, chapter_id):
        """Gets report chapter authors. gets photo and id, but not gender and citizenship"""
        params = f'q={report_id}&p={chapter_id}'
        url = f'https://apps.ipcc.ch/report/authors/authors.php?{params}'
        print(url)
        soup = self.get_soup(url)
        authors = []
        for ix, author in enumerate(soup.select('.mix')):
            author_name = author.select_one('span.author').text.title()
            last, first = re.match("([^,]+) ?, (.*)", author_name).groups()
            affiliation = author.find('font')
            cur_aff = affiliation.contents[0] if len(affiliation) > 2 else None
            authors.append({
                'index' : ix,
                'role' : author['data-role'],
                'person' : {
                    'id': int(author.select_one('span.author')['data-cid']),
                    'last name': last,
                    'first name': first,
                    'country': affiliation.contents[-1],
                    'current affiliation': cur_aff,
                    'photo': self.full_url(url, author.find('img')['src']) }
            })
        return authors

    def save_report_json(self):
        """scrape and ipcc_report_list.json file"""
        reports = self.get_reports()
        self.save_to_json(self.reports_filename, reports)

    def load_reports(self, reload=False):
        """looks for saved json file unless reload is true, then scrapes from IPCC"""
        if reload or (not self.json_file_exists(self.reports_filename)):
            self.save_report_json()
        self.reports = self.json_load(self.reports_filename)
