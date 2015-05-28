import requests
from bs4 import BeautifulSoup
import re


def scrape_NYC_metal_scene():
    url = 'http://nycmetalscene.com/'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text)
    shows = [show.text for show in soup.findAll('td', id=re.compile('^Text2'))]
    return shows[2:]

print '\n'.join(scrape_NYC_metal_scene())
