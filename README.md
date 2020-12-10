# Telegram client Docker image

This Docker image provides a client to login and send messages to the [Telegram](https://telegram.org/) messenger.

The image uses the [Telethon](https://github.com/LonamiWebs/Telethon) library which is an awesome MTProto API Telegram client written
in Python.

The `telegram-client` Docker image serves these functionalities.

* Obtain session token
* Send messages to Telegram

## Preparations

To use this image you need a proper Telegram account as well as a Telegram API account for development. The Docker image needs the account 
information to connect with the messenger via application API provided by Telegram.

### Create a Telegram API account

Go and visit [https://my.telegram.org/](https://my.telegram.org/) to create a new development API account. You will be prompted for your phone number that
 is used in your Telegram account and you will have to prove a proper phone code as authorization. 
 
Once you have signed up for a development account you will be provided with an `app_id` and `app_hash`. Please keep 
 this information for later usage (but keep this information private as it is linked to your personal Telegram account and allows access to it).
 
In addition to that you will be provided with a test configuration in particular the DC identifier (a number 1-3) and a test server IP address. 
We also need this information later in the process.

### Create an account/bot in the Telegram test space

Telegram provides a separate set of test servers 
that can be used for testing. It is a good idea to use this test environment because messages will be periodically wiped 
and we will not hit rate limits (e.g. for login attempts) of our private Telegram accounts when running the tests multiple 
times in a CI pipeline.

As the Telegram test space is completely separated from the production space you need to recreate your accounts and bots there once more. 

You can create test accounts when connecting in [Telegram test mode](https://web.telegram.org/?test=1).
Please do a complete new signup with your phone number in test mode. Do not share private information on this test account 
as it may be exposed to lower security standards on that test environment.

Once you have a test account go to `@BotFather` and create a bot as usual. To access the HTTP bot API in the Telegram test 
space just add `/test` to the end of your bot token.

```
https://api.telegram.org/bot{your-bot-token}/test/getMe
``` 

Now you have a test account and a test bot in the Telegram test space.

## Obtain session token

You can use this image to login into your Telegram account in order to receive a session token you can reuse in subsequent API calls
as long as you keep the session alive on your account.

This is a nice way to connect with Telegram in a CI/CD pipeline where automated tests need to exchange messages
with Telegram and manual interaction needs to be avoided. The usual Telegram login procedure involves a phone number and 
phone code where latter gets sent to you via SMS or Telegram itself. This is why we want to use the session token for 
automated tests instead. 

Please be sure to use the [Telegram test space](https://web.telegram.org/?test=1) for such automated testing. 

The image uses [Telethon](https://docs.telethon.dev/en/latest/) as client. Telethon is written in Python and supports 
session token based login.

In order to obtain a valid session token we have to perform the usual Telegram login procedure. We can then reuse the session 
token in all subsequent calls in our automated tests. 

The Docker image uses a set of environment variables that a user needs to provide. Please fill out the following parameters 
in a new properties file.

_telegram-client.properties_
```
TELEGRAM_DC_ID=2
TELEGRAM_DC_IP=149.154.167.40
TELEGRAM_API_ID=
TELEGRAM_API_HASH=
TELEGRAM_USERNAME=@bot_name
TELEGRAM_TEXT=Howdy
```            

Please use the Telegram API account information. If you do not have the yet please go back to the preparation steps in this guide.

Now get the session token from the Telegram login.
 
_Run yaks/telegram-client login_
```shell script
docker run -i --rm --env-file telegram-client.properties yaks/telegram-client python3 /app/login.py
```

The Docker container uses interactive mode because you have to provide a proper phone number and phone code to verify the login. 
As a result a session token gets printed to the container output. Copy and save this session token for future usage into the `telegram-client.properties`.

```
TELEGRAM_SESSION={session_string}
```

## Send messages to Telegram

Now we can test the session token to send messages to the Telegram messenger.

```shell script
docker run -i --rm --env TELEGRAM_TEXT=Howdy --env-file telegram-client.properties yaks/telegram-client
```

You should see the message on your Telegram chat/bot now.

Please add the account information to the file `telegram-credentials.properties` so the test
can use it to connect to the Telegram API.
