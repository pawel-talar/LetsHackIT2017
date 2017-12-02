import json
import logging

competition_list_key = 'competitions'
answers_list_key_format = 'answers_{comp_id}'

competition_id = 'competition_{id}'


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
    id = redis_client.rpush(adding_point, serialized_comp) - 1
    return id


def get_task(redis_client, competition_id, task_id):
    assert type(task_id) == int
    return redis_client.lindex('tasks_{}'.format(competition_id), task_id)


def get_competition(redis_client, competition_id):
    assert type(competition_id) == int
    return redis_client.lindex(competition_list_key, competition_id)


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


def check_task_answer(redis_client, competition_id, task_id, answer):
    assert redis_client is not None
    assert type(competition_id) == str
    assert type(task_id) == str
    assert len(competition_id) > 0
    assert len(task_id) > 0
    assert competition_id.isdigit()
    assert task_id.isdigit()
    logging.info("Checking answer {} for task {} in competition {}".format(
        answer, task_id, competition_id))
    task_json = redis_client.lindex('tasks_{}'.format(competition_id),
                                 int(task_id))
    if task_json is None:
        raise ValueError('Zadanie o id = {} w konkursie nr {} nie '
                          'istnieje'.format(task_id, competition_id))

    task = json.loads(task_json.decode())
    logging.info("Loaded task for answer checking: {}".format(task))
    if task is None:
        return False
    assert type(task) == dict
    assert type(task['ans']) == str
    return task['ans'].strip() == answer.strip()


def submit_correct_answer(redis_client, competition_id, task_id, user_id):
    assert type(competition_id) == int
    assert type(task_id) == int
    assert type(user_id) == int
    correct_answer = {'task_id': task_id, 'user_id': user_id}
    correct_answer_json = json.dumps(correct_answer)
    logging.info("Saving correct answer: {}".format(correct_answer))
    redis_client.rpush(answers_list_key_format.format(comp_id=competition_id), correct_answer_json)
  


def register_user(redis_client, user_id, comp_id):
    assert redis_client is not None
    assert type(user_id) == int and type(comp_id) == int
    if comp_id <= redis_client.llen(competition_list_key) and comp_id >= 0:
        redis_client.sadd(competition_id.format(id = comp_id), user_id)
        return True
    return False


def get_contestants(redis_client, comp_id):
    assert redis_client is not None
    assert type(comp_id) == int
    contestants = redis_client.smembers(competition_id.format(id = comp_id))
    return list(contestants)

def answers_ranking(redis_client, comp_id):
    size = redis_client.llen(answers_list_key_format.format(comp_id = comp_id))
    list=[]
    for i in range(0, size):
        list.append(redis_client.lindex(answers_list_key_format.format(comp_id = comp_id), i))
    return list