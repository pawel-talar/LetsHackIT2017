import json
from db.comp import answers_ranking


def answers_ranking_parse(redis_client, bot, update):
    assert len(update.message.text.split()) > 1
    assert update.message.text.split()[1].isdigit()
    result = []
    temp = []
    for each in answers_ranking(redis_client, update.message.text.split()[1]):
        each = each.decode()
        each = json.loads(each)
        print(each)
        tid = each['task_id']
        uid = each['user_id']
        pair = [uid, tid]
        print(pair)
        if pair not in temp:
            temp.append(pair)
    sorted(temp)
    print(temp)
    count = 1
    size = len(temp)
    for i in range(1, size):
        if temp[i][0] != temp[i - 1][0]:
            result.append([temp[i - 1][0], count])
            count = 1
            continue
        count = count + 1
    result.append([temp[size - 1][0], count])
    sorted(result)
    size = len(result)
    for i in range(0, min(size, 5)):
        show_user = lambda x: '{} {}'.format(x['first_name'], x['last_name'])
        full_name = show_user(bot.get_chat(result[i][0]))

        text = str(i + 1) + ". " + full_name + " SCORE: " + str(result[i][1])
        bot.send_message(chat_id=update.message.chat_id, text=text)