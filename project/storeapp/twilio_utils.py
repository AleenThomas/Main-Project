# twilio_utils.py
from twilio.rest import Client

def send_sms(recipient_number, message):
    # Your Twilio credentials
    account_sid = 'AC72d0d232baf2a2fba6788361351e6a46'
    auth_token = '6e9f1f907246740d18f121972c80aec7'

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    try:
        # Send SMS message
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body='Your Booking has been successful',
            to='whatsapp:+917510284058'
        )
        print("Message sent successfully:", message.sid)
        return True
    except Exception as e:
        print("Failed to send message:", str(e))
        return False