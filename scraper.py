"""scraper.py"""
import sys
import os.path as path
import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

class Scraper:
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        self.headers = {'User-Agent' : self.user_agent}

    def get_url(self, url):
        """get url with error checking"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print ("HTTP Error:", errh, errh.response.text)
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print (err)
        return response

    def get_json(self, url):
        """get json from url"""
        return self.get_url(url).json()

    def get_table(self, url):
        """use pandas to return list from HTML table in URL"""
        try:
            return pd.read_html(self.get_url(url).text)[0].to_dict('records')
        except: # no table
            return None

    @staticmethod
    def lowercase_keys(dict):
        """lowercases the keys of a dict"""
        return {key.lower(): val for key, val in dict.items()}

    @staticmethod
    def full_url(base_url, relative_href):
        """returns full url given base_url and relative_href"""
        return urljoin(base_url, relative_href)

    @staticmethod
    def json_load(filename):
        """load json from filename. wraps json"""
        with open(f'{filename}.json') as json_file:
            return json.load(json_file)

    @staticmethod
    def json_file_exists(filename):
        """check if filename.json exists"""
        return path.exists(f'{filename}.json')

    @staticmethod
    def save_to_json(filename, var):
        """write var (should be a list or dict) to json file with filename"""
        filename = filename.lower().replace(" ","_")
        with open(f'{filename}.json', 'w', encoding='utf-8') as json_f:
            json.dump(var, json_f, ensure_ascii=False, indent=4)

    @staticmethod
    def expand_df_list_column(df, expand_col, index):
        """Expand dataframe on expand_col, matching on index.
        Index can be single column name or list of column names."""
        if type(index) is not list: index = [index]
        df_indices = [df[ix] for ix in index]
        df2 = pd.DataFrame(df[expand_col].tolist(), index=df_indices) \
                .stack() \
                .reset_index() \
                .drop(columns=f'level_{len(index)}')
        return df.drop(columns=expand_col) \
                .merge(df2.drop(columns=0) \
                       .join(df2[0].apply(pd.Series), rsuffix=f'_{expand_col}'),
                 on=index)

    @staticmethod
    def expand_df_dict_column(df, expand_col):
        """Expand dataframe on expand_col"""
        return df.drop(columns=expand_col) \
                 .join(df[expand_col].apply(pd.Series),
                       rsuffix=f'_{expand_col}')

    @staticmethod
    def as_df(var):
        """Return var as DataFrame."""
        return pd.DataFrame(var)

    def get_soup(self, url):
        """get BeatifulSoup from url"""
        return BeautifulSoup(self.get_url(url).text, 'html.parser')
