import requests
import re
import arrow
from bs4 import BeautifulSoup


def scrape_NYC_metal_scene():
    url = 'http://nycmetalscene.com/'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text)
    shows_text = [show.text for show in
                  soup.findAll('td', id=re.compile('^Text2'))]
    shows = []
    for show in shows_text[2:]:
        show_split = show.split(':')
        date_text, show_text = show_split[0], show_split[1]
        date_text = re.sub(r"(st|nd|rd|th),", ",", date_text).replace('.', '')

        print date_text
        try:
            show_date = arrow.get(date_text, 'ddd MMM D, YYYY')
        except arrow.parser.ParserError:
            show_date = arrow.get(date_text, 'ddd MMMM D, YYYY')

        shows.append((show_date, show_text))
    return shows

print scrape_NYC_metal_scene()
