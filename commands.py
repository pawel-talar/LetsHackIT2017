import start
import functools
from comp.comp_register import comp_register
from comp.comp_list import comp_list

def get_commands(redis_client):
    return {
        'start': start.start,
        'comp_register': functools.partial(comp_register, redis_client),
        'comp_list': functools.partial(comp_list, redis_client)
    }