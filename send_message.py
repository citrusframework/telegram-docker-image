import os

from telethon.sync import TelegramClient
from telethon.sessions import StringSession

def send(dc_id, dc_ip, api_id, api_hash, session_str, username, text):
    client = TelegramClient(StringSession(session_str), api_id, api_hash)
    client.session.set_dc(dc_id, dc_ip, 80)
    with client:
        client.send_message(username, text)

if __name__ == '__main__':
    arg_dc_id = int(os.environ["TELEGRAM_DC_ID"])
    arg_dc_ip = os.environ["TELEGRAM_DC_IP"]
    arg_api_id = int(os.environ["TELEGRAM_API_ID"]) # https://my.telegram.org/apps
    arg_api_hash = os.environ["TELEGRAM_API_HASH"]
    arg_session_str = os.environ["TELEGRAM_SESSION"]
    arg_username = os.environ["TELEGRAM_USERNAME"]
    arg_text = os.environ["TELEGRAM_TEXT"]

    send(arg_dc_id, arg_dc_ip, arg_api_id, arg_api_hash, arg_session_str, arg_username, arg_text)
