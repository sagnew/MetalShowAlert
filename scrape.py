import requests
import re
import arrow
from bs4 import BeautifulSoup


def scrape_NYC_metal_scene():
    '''
    Returns an array of dictionaries representing each upcoming metal show
    from nycmetalscene.com.

    The dictionaries are structured as:
        {
            'original_date_text': The date text scraped from the website.
            'show_date': The arrow object representing the date of the show.
            'information': The text containing bands and venue information.
        }
    '''

    def get_date_text(scraped_text):
        '''
        scraped_text: The raw scraped text
                      representing the date of a show.

        Returns a formatted version of the text for arrow to parse.
        '''

        # Accounts for some dates that have a "." and for multi-day events.
        # Also makes September events compatible with arrow.
        return re.sub(r"(st|nd|rd|th),", ",", scraped_text) \
            .replace('.', '').split('&')[0].replace('Sept', 'Sep')

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

        date_text = get_date_text(original_date_text)

        try:
            # Check for abbreviated months.
            show_date = arrow.get(date_text, 'ddd MMM D, YYYY')

            shows.append({
                'original_date_text': original_date_text,
                'show_date': show_date,
                'information': show_text
            })
            continue
        except arrow.parser.ParserError:
            pass
        try:
            # Check for unabbreviated months.
            show_date = arrow.get(date_text, 'ddd MMMM D, YYYY')

            shows.append({
                'original_date_text': original_date_text,
                'show_date': show_date,
                'information': show_text
            })
            continue
        except arrow.parser.ParserError:
            pass
        try:
            # Check for missing year.
            show_date = arrow.get(date_text, 'ddd MMM D')

            shows.append({
                'original_date_text': original_date_text,
                'show_date': show_date,
                'information': show_text
            })
            continue
        except arrow.parser.ParserError:
            pass
        try:
            # Check for missing year, and unabbreviated month.
            show_date = arrow.get(date_text, 'ddd MMMM D')

            shows.append({
                'original_date_text': original_date_text,
                'show_date': show_date,
                'information': show_text
            })
            continue
        except arrow.parser.ParserError:
            # This means that our parser caught something that wasn't a show
            # or it had a date so badly formatted, that it was deemed unworthy.
            print 'Error parsing: %s' % date_text
            continue

    return shows

for show in scrape_NYC_metal_scene():
    print show['original_date_text']
    print show['information']
    print '\n'
