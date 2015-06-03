from twilio.rest import TwilioRestClient
import arrow
from scrape import scrape_NYC_metal_scene, scrape_SF_list
from secrets import account_sid, auth_token
from numbers import my_cell_phone, twilio_number

client = TwilioRestClient(account_sid, auth_token)

def get_show_messages(city):
    # shows = scrape_NYC_metal_scene()
    shows = scrape_SF_list()
    shows_this_week = []
    for show in shows:
        show_ts = show['show_date'].timestamp
        now = arrow.now()
        next_week = now.replace(weeks=+1).timestamp
        if show_ts >= now.timestamp and show_ts < next_week:
            shows_this_week.append(show)
    shows_this_week = sorted(shows_this_week, key=lambda x: x['show_date'].timestamp)

    show_messages = []
    message_body = 'Shows in ' + city + ' this week:\n'
    for show in shows_this_week:
        show_text = show['original_date_text'] + ' ' + show['information'] + '\n'
        if len(message_body) + len(show_text) > 1600:
            show_messages.append(message_body)
            message_body = 'More shows in ' + city + ' this week:\n' + show_text
        else:
            message_body = message_body + show_text
    show_messages.append(message_body)

    return show_messages

def send_show_messages(city):
    show_messages = get_show_messages(city)
    for show_message in show_messages:
        message = client.messages.create(to=my_cell_phone, from_=twilio_number,
                                         body=show_message)
