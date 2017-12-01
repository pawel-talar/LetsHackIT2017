def start(bot, update):
    assert bot is not None
    text = 'Ty kurwo, zmarnowałaś mi 20 lat życia'
    bot.send_message(chat_id=update.message.chat_id, text=text)