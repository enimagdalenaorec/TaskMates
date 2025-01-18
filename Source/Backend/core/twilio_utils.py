from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant
from chat_secrets import TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, TWILIO_CHAT_SERVICE_SID

def generate_twilio_token(identity):
    # Replace with your Twilio credentials
    account_sid = TWILIO_ACCOUNT_SID
    api_key = TWILIO_API_KEY
    api_secret = TWILIO_API_SECRET
    chat_service_sid = TWILIO_CHAT_SERVICE_SID

    # Create access token
    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    # Add Chat grant
    chat_grant = ChatGrant(service_sid=chat_service_sid)  # Provjeri da je varijabla ispravno definirana
    token.add_grant(chat_grant)  # Ovdje može biti prekinuta linija u tvom kodu

    return token.to_jwt()  # Ovdje bi sada trebalo raditi bez greške
