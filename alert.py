from alert_utils import send_show_messages
import db_utils

for user in db_utils.get_users_by_city('sf'):
    number = user['number']
    print 'Sending shows to %s' % number
    send_show_messages(number, 'SF')

for user in db_utils.get_users_by_city('nyc'):
    number = user['number']
    print 'Sending shows to %s' % number
    send_show_messages(number, 'NYC')
