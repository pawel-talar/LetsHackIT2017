from db.comp import register_competition

def comp_register(redis_client, bot, update):
    assert bot is not None
    comp_params = update.message.text.split()[1:]
    assert len(comp_params) >= 2
    name, desc = comp_params[0], ' '.join(comp_params[1:])
    print((name, desc))
    register_competition(redis_client, name, desc)


