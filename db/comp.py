import json

competition_list_key = 'competitions'

def register_competition(redis_client, name, description):
    assert redis_client is not None
    assert type(name) == str
    assert type(description) == str
    comp = {'name': name, 'desc': description}
    serialized_comp = json.dumps(comp)
    redis_client.rpush(competition_list_key, serialized_comp)


def add_task(redis_client, competition_id, name, description, answer):
    assert type(name) == str
    assert type(description) == str
    comp = {'competition_id': competition_id, 'name': name, 'desc': description, 'ans': answer}
    serialized_comp = json.dumps(comp)
    adding_point = "tasks_{}".format(competition_id)
    redis_client.rpush(adding_point, serialized_comp)

def comps_list(redis_client):
    text = ''
    for i, c in enumerate(redis_client.lrange('competitions', 0, -1)):
        t = json.loads(c.decode())
        text = text + '\n' + "{}: {}\n {}".format(i, t['name'], t['desc'])
    return text

def comp_tasks(redis_client, comp_id):
    text = ''
    for i, c in enumerate(redis_client.lrange("tasks_{}".format(comp_id), 0, -1)):
       t = json.loads(c.decode())
       text = text + '\n' + "{}: {}\n {}".format(i, t['name'], t['desc'])
    return text