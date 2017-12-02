import json
import codecs
from db.comp import answers_ranking


def answers_ranking_parse(redis_client, bot, update):
    result = []
    temp = []
    for each in answers_ranking(redis_client, 2):
        each = codecs.decode(each)
        to_parse = each.split()[1:]
        tid = to_parse[0][:-1]
        uid = to_parse[-1][:-1]
        pair = [uid, tid]
        if pair not in temp:
            temp.append(pair)

    sorted(temp)
    count = 1
    size = len(temp)
    for i in range(1, size):
        if temp[i][0] != temp[i - 1][0]:
            result.append([temp[i][0], count])
            count = 1
        count = count + 1
    result.append([temp[size - 1][0], count])
    sorted(result)
    size = len(result)
    for i in range(0, min(size, 5)):
        show_user = lambda x: '{} {}'.format(x['first_name'], x['last_name'])
        full_name = '\n'.join([show_user(bot.get_chat(contestant.decode())) for contestant in
                               get_contestants(redis_client, competition_id)])

        text = str(i + 1) + ". " + str(result[i][0]) + " SCORE:" + str(result[i][1])
        bot.send_message(chat_id=update.message.chat_id, text=text)

        show_user = lambda x: '{} {}'.format(x['first_name'], x['last_name'])
        full_name = '\n'.join([show_user(bot.get_chat(contestant.decode())) for
                               contestant in get_contestants(redis_client, competition_id)])
