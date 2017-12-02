from db.comp import comp_tasks

def comp_tasks_list(redis_client, bot, update):
    comp_id = update.message.text.split()[1]
    assert comp_id.isdigit()
    text = comp_tasks(redis_client, comp_id)
    if text != '':
        bot.send_message(chat_id=update.message.chat_id, text=text)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Brak pytań dla tego konkursu!')

