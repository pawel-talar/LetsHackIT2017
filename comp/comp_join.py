from db.comp import register_user

def user_comps_register(redis_client, bot, update):
    assert bot is not None and update is not None
    comp_list = update.message.text.split()[1:]
    text = "Pomyslnie zapisales sie do konkursow:"
    for c in comp_list:
        if register_user(redis_client, update.message.from_user.id, int(c)):
            text = text + " " + str(c)
    bot.send_message(chat_id=update.message.chat_id, text=text)