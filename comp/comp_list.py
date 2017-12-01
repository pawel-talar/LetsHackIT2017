import json

def comp_list(redis_client, bot, update):
    text = ''
    for i, c in enumerate(redis_client.lrange('competitions', 0, -1)):
        t = json.loads(c.decode())
        text = text + '\n' + "{}: {} {}".format(i, t['name'], t['desc'])
    bot.send_message(chat_id=update.message.chat_id, text=text)
