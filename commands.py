import start
import functools
from comp.comp_register import comp_register
from comp.comp_list import comp_list
from comp.comp_add_task import comp_add_task
from comp.comp_join import user_comps_register

def get_commands(redis_client):
    return {
        'start': start.start,
        'comp_register': functools.partial(comp_register, redis_client),
        'comp_list': functools.partial(comp_list, redis_client),
        'comp_add_task': functools.partial(comp_add_task, redis_client),
        'comp_join': functools.partial(user_comps_register, redis_client)
    }