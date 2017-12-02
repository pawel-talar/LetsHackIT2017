from config import config_reader
from db.comp import register_competition
from db.comp import add_task
import os
import redis

default_config_filename = os.path.abspath('config.yaml')


if __name__ == '__main__':
    redis_config = config_reader.get_redis_address_from_config(default_config_filename)
    redis_client = redis.StrictRedis(host=redis_config['ip'],
                                     port=redis_config['port'],
                                     db=0)

    competitions = [
        {'name': 'lets-hack-it', 'description': 'Hackaton dla studentów'},
        {'name': 'advent-of-code-2017', 'description': 'Help Santa Claus '
                                                       'before Christmas'},
    ]
    for comp in competitions:
        register_competition(redis_client, comp['name'], comp['description'])

    tasks = {
        0: [
            {'name': 'Symulacje', 'description': 'Credit?', 'answer': 'Suisse'},
            {'name': 'Boty', 'description': '5+3?', 'answer': '8'},
        ],
        1: [
            {'name': 'Stars', 'description': 'Lowest prime number?', 'answer':
                '2'},
            {'name': 'Snow', 'description': 'ROT13(ala)?', 'answer': 'nyn'},
        ]
    }

    for i, ts in tasks.items():
        for t in ts:
            add_task(redis_client, i, t['name'], t['description'], t['answer'])
