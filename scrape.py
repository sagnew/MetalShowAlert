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
    for show in shows_text[2:]:
        show_split = show.split(':')
        original_date_text, show_text = show_split[0], ':'.join(show_split[1:])

        date_text = get_date_text(original_date_text)

        show_dict = {
            'original_date_text': original_date_text,
            'information': show_text
        }
        try:
            # Check for abbreviated months.
            show_date = arrow.get(date_text, 'ddd MMM D, YYYY')

            show_dict['show_date'] = show_date
            shows.append(show_dict)
            continue
        except arrow.parser.ParserError:
            pass
        try:
            # Check for unabbreviated months.
            show_date = arrow.get(date_text, 'ddd MMMM D, YYYY')

            show_dict['show_date'] = show_date
            shows.append(show_dict)
            continue
        except arrow.parser.ParserError:
            pass
        try:
            # Check for missing year.
            show_date = arrow.get(date_text, 'ddd MMM D')

            show_dict['show_date'] = show_date
            shows.append(show_dict)
            continue
        except arrow.parser.ParserError:
            pass
        try:
            # Check for missing year, and unabbreviated month.
            show_date = arrow.get(date_text, 'ddd MMMM D')

            show_dict['show_date'] = show_date
            shows.append(show_dict)
            continue
        except arrow.parser.ParserError:
            # This means that our parser caught something that wasn't a show
            # or it had a date so badly formatted, that it was deemed unworthy.
            print 'Error parsing: %s' % date_text
            continue

    return shows

def scrape_SF_list():
    '''
    Returns an array of dictionaries representing each upcoming metal show
    from 'The List' of San Francisco shows.

    The dictionaries are structured as:
        {
            'original_date_text': The date text scraped from the website.
            'show_date': The arrow object representing the date of the show.
            'information': The text containing bands and venue information.
        }
    '''
    url = 'http://www.foopee.com/punk/the-list/by-date.0.html'
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text)

    result_dict = {}

    # gives the first unordered list as its own object
    shows_element = soup.select('ul')[0]
    weekly_shows = shows_element.select('li ul')

    # weekly shows by index in shows_element object
    for i, show in enumerate(weekly_shows):
        date_text = shows_element.select('li a[name]')[i].text
        result_dict[date_text] = \
                [show.text.strip('\n') for show in weekly_shows[i].select('li')]

    shows = []
    for date_text in result_dict.keys():
        year = str(arrow.now().year)
        show_date = arrow.get(date_text + ' ' + year, 'ddd MMM D YYYY')
        for show_info in result_dict[date_text]:
            show_dict = {
                    'original_date_text': date_text,
                    'show_date': show_date,
                    'information': show_info
            }
            shows.append(show_dict)
            show_info = ''

    return shows

print scrape_SF_list()[0]
