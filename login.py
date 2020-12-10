import os

from telethon.sync import TelegramClient
from telethon.sessions import StringSession

def login(dc_id, dc_ip, api_id, api_hash):
    client = TelegramClient(StringSession(), api_id, api_hash)
    client.session.set_dc(dc_id, dc_ip, 80)
    with client:
        print("Your session string is:", client.session.save())

if __name__ == '__main__':
    arg_dc_id = int(os.environ["TELEGRAM_DC_ID"])
    arg_dc_ip = os.environ["TELEGRAM_DC_IP"]
    arg_api_id = int(os.environ["TELEGRAM_API_ID"]) # https://my.telegram.org/apps
    arg_api_hash = os.environ["TELEGRAM_API_HASH"]

    login(arg_dc_id, arg_dc_ip, arg_api_id, arg_api_hash)
