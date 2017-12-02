from db.comp import add_task
from db.comp import get_task
from db.comp import get_competition
from db.comp import get_contestants
import logging


def notify_user(redis_client, bot, user_id, competition_id, name, task_id):
    assert bot is not None
    assert type(user_id) == int
    assert type(competition_id) == int
    assert type(task_id) == int
    competition = get_competition(redis_client, competition_id)
    assert competition is not None
    task = get_task(redis_client, competition_id, task_id)
    assert task is not None
    text = "Nowe zadanie w konkursie {}\n{}\n".format(competition_id, name)
    bot.send_message(chat_id=user_id, text=text)


def comp_add_task(redis_client, bot, update):
    assert bot is not None
    comp_params = update.message.text.split()[1:]
    assert len(comp_params) >= 2
    competition_id, name, desc, answer = comp_params[0], comp_params[1], ' '.join(comp_params[2:-1]), comp_params[-1]
    logging.info("Adding task for contest {}".format(int(competition_id)))
    id = add_task(redis_client, competition_id, name, desc, answer)
    assert id is not None
    competition_id = int(competition_id)
    contestants = get_contestants(redis_client, competition_id)
    assert type(contestants) == list
    logging.info("Registered contestants {}".format(contestants))
    for contestant in contestants:
        logging.info("Notifying user {}".format(int(contestant)))
        notify_user(redis_client, bot, int(contestant), int(competition_id), name, id)
