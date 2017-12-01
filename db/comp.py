import json

competition_list_key = 'competitions'


def register_competition(redis_client, name, description):
    assert redis_client is not None
    assert type(name) == str
    assert type(description) == str
    comp = {'name': name, 'desc': description}
    serialized_comp = json.dumps(comp)
    redis_client.lpush(competition_list_key, serialized_comp)