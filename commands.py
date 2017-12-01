import start
import functools
from comp.comp_register import comp_register

def get_commands(redis_client):
    return {
        'start': start.start,
        'comp_register': functools.partial(comp_register, redis_client)
    }