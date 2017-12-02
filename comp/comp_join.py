from db.users import register_user

def user_comps_register(redis_client, bot, update):
    assert bot is not None
    assert update is not None
    comp_list = update.message.text.split()
    register_user(redis_client, update.message.from_user.id, comp_list)
    text = 'Pomyślnie zapisałeś się do konkursów'
    bot.send_message(chat_id=update.message.chat_id, text=text)