from db.comp import add_task

def comp_add_task(redis_client, bot, update):
    assert bot is not None
    comp_params = update.message.text.split()[1:]
    assert len(comp_params) >= 2
    competition_id, name, desc, answer = comp_params[0], comp_params[1], ' '.join(comp_params[2:-1]), comp_params[-1]
    print((name, desc, answer))
    add_task(redis_client, competition_id, name, desc, answer)

