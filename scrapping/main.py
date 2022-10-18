from scrapping.bot import Bot
from bs4 import BeautifulSoup

if __name__ == "__main__":
    b = Bot()
    b.get_links()
    b.read_table()