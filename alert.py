from twilio.rest import TwilioRestClient
import arrow
from secrets import account_sid, auth_token
from numbers import my_cell_phone, twilio_number
from scrape import scrape_NYC_metal_scene

client = TwilioRestClient(account_sid, auth_token)

shows = scrape_NYC_metal_scene()
shows_this_week = []
for show in shows:
    show_ts = show['show_date'].timestamp
    now = arrow.now()
    next_week = now.replace(weeks=+1).timestamp
    if show_ts >= now.timestamp and show_ts < next_week:
        shows_this_week.append(show)

message_body = 'Shows in NYC this week:\n'
for show in shows_this_week:
    show_text = show['original_date_text'] + ' ' + show['information'] + '\n'
    message_body = message_body + show_text

message = client.messages.create(to=my_cell_phone, from_=twilio_number,
                                 body=message_body)
