from config import config_reader
from db.comp import register_competition
import os
import redis

default_config_filename = os.path.abspath('config.yaml')


if __name__ == '__main__':
    redis_config = config_reader.get_redis_address_from_config(default_config_filename)
    redis_client = redis.StrictRedis(host=redis_config['ip'],
                                     port=redis_config['port'],
                                     db=0)

    competitions = [
        {'name': 'lets-hack-it', 'description': 'Hackaton for students'},
        {'name': 'advent-of-code-2017', 'description': 'Help Santa Claus'}
    ]
    for comp in competitions:
        register_competition(redis_client, comp['name'], comp['description'])