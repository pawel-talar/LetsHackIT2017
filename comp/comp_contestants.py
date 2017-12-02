from db.comp import get_contestants


def comp_contestants(redis_client, bot, update):
    assert redis_client is not None
    params = update.message.text.split()[1:]
    assert len(params) == 1
    competition_id_str = params[0]
    assert competition_id_str.isdigit()
    competition_id = int(competition_id_str)

    show_user = lambda x: '{} {}'.format(
        x['first_name'], x['last_name'])
    text = '\n'.join([show_user(bot.get_chat(contestant.decode())) for
                     contestant in get_contestants(redis_client, competition_id)])

    bot.send_message(chat_id=update.message.chat_id, text=text)