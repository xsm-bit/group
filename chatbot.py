from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackContext)
import configparser
import os
import logging
import redis
from ChatGPT_HKBU import HKBU_ChatGPT

global redis1


def main():
    # Load your token and create an Updater for your Bot

    #using config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    # updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)

    updater =Updater(token=(os.environ['TLG_ACCESS_TOKEN']),use_context=True)
    print(os.environ['TLG_ACCESS_TOKEN'])
    print('here----------------------------')
    dispatcher = updater.dispatcher
    global redis1
    '''
    redis1 = redis.Redis(host=(config['REDIS']['HOST']), password=(config['REDIS']['PASSWORD']),
                         port=(config['REDIS']['PORT']))
    '''
    redis1 = redis.Redis(host=(os.environ['REDIS_HOST']), password=(os.environ['REDIS_PASSWORD']),
                         port=(os.environ['REDIS_PORT']))

    # You can set this logging module, so you will know when and why things do not work as expected Meanwhile, update your config.ini as:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # register a dispatcher to handle message: here we register an echo dispatcher
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)

    # dispatcher for chatgpt
    logging.info("config: " + str(config))
    print(config)
    print('----------------------------------')
    global chatgpt
    #chatgpt = HKBU_ChatGPT(config)
    chatgpt = HKBU_ChatGPT(os.environ['GPT_TOKEN'])
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("help", help_command))

    # To start the bot:
    updater.start_polling()
    updater.idle()


def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


def equiped_chatgpt(update, context):
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    print(update)
    print(context)
    print(update.message.text)
    print('------------')
    add(update, context, update.message.text)
    print(update)
    if update.message.text=='/hello Kevin':
        reply_message='Good day, Kevin!'
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')

'''
def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]  # /add keyword <-- this should store the keyword
        print(msg)
        redis1.incr(msg)
        update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')
'''
def add(update, context, message):
    global redis1
    keyword = message  # 将整个消息作为关键字
    logging.info(keyword)
    redis1.incr(keyword)
    #update.message.reply_text('You have said ' + keyword + ' for ' + redis1.get(keyword).decode('UTF-8') + ' times.')

if __name__ == '__main__':
    main()

