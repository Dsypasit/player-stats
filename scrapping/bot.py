from unittest import result
from bs4 import BeautifulSoup
import urllib.request
import urllib.robotparser as rb
import pandas as pd
from lxml import etree

class Bot:

    def __init__(self):
        self.base_url = r'https://fbref.com'
        self.url = r'https://fbref.com/en/comps/Big5/Big-5-European-Leagues-Stats'
        self.robot_url = r'https://fbref.com/robots.txt'
        self.team_links = []
    
        self.bot = rb.RobotFileParser()
        self.bot.set_url(self.robot_url)
        self.bot.read()
    
    def request(self, url=""):
        if url == "":
            url=self.url

        if self.bot.can_fetch("*", url):
            try:
                result = urllib.request.urlopen(url)
                return result.read()
            except Exception as e:
                print(str(e))
                return None
        return None
    
    def get_links(self):
        result = self.request()
        soup = BeautifulSoup(result, 'html.parser')
        table = soup.find(id="big5_table")
        inside_table = soup.find('tbody')
        rows = inside_table.find_all('tr')
        for row in rows:
            a_tags = row.find('a')
            self.team_links.append(self.base_url+a_tags['href'])
    
    def read_table(self):
        for link in self.team_links[-1:-10:-1]:
            content = self.request(link)
            self._find_filter(content)
    
    def _find_filter(self, content):
        # //*[@id="content"]/div[2]/div[1]/a
        soup = BeautifulSoup(content, 'html.parser')
        dom = etree.HTML(str(soup))
        l = dom.xpath('//*[@id="content"]/div[2]/div[1]/a/@href')
        if len(l) >0:
            content = self.request(self.base_url+l[0])
            # content = BeautifulSoup(result, 'html.parser')
        # print(type(content))
        df = pd.read_html(str(content))
        print(df[0].head())
        
