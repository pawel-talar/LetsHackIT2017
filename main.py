import commands
from config import config_reader
import logging
import os.path
import redis
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

default_config_filename = os.path.abspath('config.yaml')


def get_bot(token):
    assert type(token) == str
    assert len(token) > 0
    return telegram.Bot(token)


def get_updater(token):
    return Updater(token=token)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)

    redis_config = config_reader.get_redis_address_from_config(default_config_filename)
    redis_client = redis.StrictRedis(host=redis_config['ip'],
                                     port=redis_config['port'],
                                     db=0)

    token = config_reader.get_token_from_config(default_config_filename)
    bot = get_bot(token)
    updater = get_updater(token)

    commands = commands.get_commands(redis_client)

    dispatcher = updater.dispatcher
    for name, func in commands.items():
        handler = CommandHandler(name, func)
        dispatcher.add_handler(handler)

    updater.start_polling()