#!/usr/bin/env python 

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


import signal
def signal_handler(signal, frame):
    # logger.warning("SIGIN recv, terminating...")
    pass
    
signal.signal(signal.SIGINT, signal_handler)


from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import sys, os
import json
from functools import wraps

admin_list = json.loads(os.environ['LIST_OF_ADMINS'])
assert isinstance(admin_list, list)
assert all(isinstance(item, int) for item in admin_list)

def restricted(func):
    '''
    Adapted from https://github.com/python-telegram-bot/
    python-telegram-bot/wiki/Code-snippets#restrict-access-to-a-handler-decorator
    '''
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        chat_id = update.message.chat.id
        if user_id not in admin_list:
            logger.warning(f"Unauthorized access denied for {user_id}")
            bot.send_message(chat_id=chat_id, text="Unauthorized access")
            return
        return func(update, context, *args, **kwargs)
    return wrapped


@restricted
def cmd_start(update, context):
    chat_id = update.message.chat_id
    logger.debug(f'[chat_id:{chat_id}] Starting.')
    update.message.reply_text("You are authorized!")

from urllib.request import urlopen
@restricted
def cmd_help(update, context):
    chat_id = update.message.chat_id
    logger.debug(f'[chat_id:{chat_id}] Help.')
    response = "The following commands are available:\n"
    commands = [
        ["/start", "Check for availablility"],
        ["/find_ip", "Get the public IP"],
        ["/help", "Get this message"]
    ]
    for command in commands:
        response += command[0] + " " + command[1] + "\n"
    update.message.reply_text(response)

@restricted
def cmd_ip(update, context):
    '''
    Alternative ip check servers:
    https://cloudflare.com/cdn-cgi/trace
    http://ifconfig.co/
    '''
    chat_id = update.message.chat.id
    my_ip = urlopen('http://ip.42.pl/raw').read().decode("utf-8") 
    logger.info(f'[chat_id:{chat_id}] Getting IP: {my_ip}')
    update.message.reply_text(my_ip)

def error(update, context):
    logger.warning('Update "%s" caused error "%s"' % (update, context.error))


token = os.environ['TELEGRAM_TOKEN']
logger.info(f'TELEGRAM_TOKEN: {token[:6]}{"*"*(len(token)-12)}{token[-6:]}')
assert isinstance(token, str)

updater = Updater(token)
b = Bot(token)
logger.info(f"BotName: {b.name}")

dp = updater.dispatcher
dp.add_handler(CommandHandler("start", cmd_start))
dp.add_handler(CommandHandler("help", cmd_help))
dp.add_handler(CommandHandler("find_ip", cmd_ip))
dp.add_error_handler(error)

updater.start_polling()
logger.info("Telegram bot has started...")

updater.idle()
logger.info("Interrupted by user, quitting...")
