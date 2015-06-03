from flask import Flask, request, redirect
import twilio.twiml
from alert_utils import get_show_messages, send_show_messages
import db_utils

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def respond_with_shows():
    """Respond to incoming texts with a simple text message."""

    number = request.form['From']
    message_body = request.form['Body'].lower()

    if db_utils.get_user_by_number(number) is None:
        db_utils.insert(number, message_body)
    else:
        db_utils.update_user(number, message_body)

    if message_body in ['quit', 'q', 'stop', 'no']:
        # If the user's value in the DB is not a city, they won't be bothered.
        resp = twilio.twiml.Response()
        m = "Sorry to see you go. Text back with your city if you want back in!"
        resp.message(m)
        return str(resp)

    send_show_messages(number, message_body)

    resp = twilio.twiml.Response()
    resp.message("You will receive show updates every Monday! \
            Respond with 'quit' to stop receiving messages.")
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
