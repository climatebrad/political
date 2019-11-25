"""ipcc scraper"""

from scraper import Scraper

class IPCC(Scraper):
    def __init__(self):
        super().__init__()
        self.report_ids = self.get_report_ids()

    def get_report_ids(self):
        """load report_ids from site."""
        url = 'https://apps.ipcc.ch/report/authors/'
        return {int(option['value']) : option.text for option in
                self.get_soup(url).select('#cmbreport option') if option['value']}

    def get_report_chapter_ids(self, report_id):
        """gets json in format: [ { 'id' : #, 'description' : '..', .. """
        url = 'https://apps.ipcc.ch/report/authors/json/json.chapters.php?q=' + str(report_id)
        return { x['id'] : x['description'] for x in self.get_json(url)}
