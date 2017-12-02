from db.comp import check_task_answer
from db.comp import submit_correct_answer


def comp_submit_answer(redis_client, bot, update):
    assert bot is not None
    assert update is not None

    params = update.message.text.split()[1:]
    if len(params) != 3:
        return
    competition_id, task_id, answer = params

    try:
        result = check_task_answer(redis_client, competition_id, task_id, answer)
    except ValueError as e:
        bot.send_message(chat_id=update.message.chat_id, text="{}".format(e))
        return

    if result:
        pass_text = 'Brawo, prawidłowa odpowiedź'
        user_id = update.message.from_user.id
        submit_correct_answer(redis_client, int(competition_id), int(task_id),
                              user_id)
        bot.send_message(chat_id=update.message.chat_id, text=pass_text)
    else:
        fail_text = 'Nieprawidłowa odpowiedź'
        bot.send_message(chat_id=update.message.chat_id, text=fail_text)