import json
import logging

competition_list_key = 'competitions'
answers_list_key_format = 'answers_{comp_id}'

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
    redis_client.rpush(answers_list_key_format.format(
        comp_id=competition_id), correct_answer_json)