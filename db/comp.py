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
