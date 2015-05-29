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
    print len(shows_text[2:])
    for show in shows_text[2:]:
        show_split = show.split(':')
        original_date_text, show_text = show_split[0], ':'.join(show_split[1:])

        # Accounts for some dates that have a "." and for multi-day events.
        # Also makes September events compatible with arrow.
        date_text = re.sub(r"(st|nd|rd|th),", ",", original_date_text) \
            .replace('.', '').split('&')[0].replace('Sept', 'Sep')

        try:
            # Check for abbreviated months.
            show_date = arrow.get(date_text, 'ddd MMM D, YYYY')

            shows.append((show_date, original_date_text, show_text))
            continue
        except arrow.parser.ParserError:
            pass
        try:
            # Check for unabbreviated months.
            show_date = arrow.get(date_text, 'ddd MMMM D, YYYY')

            shows.append((show_date, original_date_text, show_text))
            continue
        except arrow.parser.ParserError:
            pass
        try:
            # Check for missing year.
            show_date = arrow.get(date_text, 'ddd MMM D')

            shows.append((show_date, original_date_text, show_text))
            continue
        except arrow.parser.ParserError:
            pass
        try:
            # Check for missing year, and unabbreviated month.
            show_date = arrow.get(date_text, 'ddd MMMM D')

            shows.append((show_date, original_date_text, show_text))
            continue
        except arrow.parser.ParserError:
            # This means that our parser caught something that wasn't a show
            # or it had a date so badly formatted, that it was deemed unworthy.
            print 'Error parsing: %s' % date_text
            continue

    return shows

print len(scrape_NYC_metal_scene())
