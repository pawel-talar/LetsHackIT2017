from db.comp import comps_list

def comp_list(redis_client, bot, update):
    text = comps_list(redis_client)
    if text != '':
        bot.send_message(chat_id=update.message.chat_id, text=text)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Nie ma konkursów!')