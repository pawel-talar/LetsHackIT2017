
competition_list_key = 'competitions'
competition_id = 'competition_{id}'

def show_my_comps(redis_client, bot, update):
    size = redis_client.llen(competition_list_key)
    text = "Twoje aktualne konkursy:"
    for i in range(0, size):
        if redis_client.sismember(competition_id.format(id=i), update.message.from_user.id) == 1:
            text = text + " " + str(i)
    bot.send_message(chat_id=update.message.chat_id, text=text)
