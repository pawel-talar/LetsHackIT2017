import json
from db.comp import answers_ranking
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from pylab import savefig

def plotting(external_names, external_scores, contest_number):
    y_pos = np.arange(len(external_names))

    external_scores = list(map(lambda x: max(0, x), external_scores))

    performance = external_scores
    plt.bar(y_pos, performance, align='center')
    plt.xticks(y_pos, external_names)
    plt.xlabel('Imię i nazwisko')
    plt.ylabel('Punkty')
    plt.title('Wyniki {} konkursu'.format(contest_number))

    savefig('plot.png', bbox_inches = 'tight')

def answers_ranking_parse(redis_client, bot, update):
    assert len(update.message.text.split()) > 1
    assert update.message.text.split()[1].isdigit()
    result = []
    temp = []
    external_scores = []
    external_names = []

    for each in answers_ranking(redis_client, update.message.text.split()[1]):
        each = each.decode()
        each = json.loads(each)
        contest_number = update.message.text.split()[1]
        print(each)
        tid = each['task_id']
        uid = each['user_id']
        pair = [uid, tid]
        print(pair)
        if pair not in temp:
            temp.append(pair)
    sorted(temp)
    count = 1
    size = len(temp)
    if size < 1:
        bot.send_message(chat_id=update.message.chat_id, text="Nie istnieje konkurs o podanym numerze")
        return
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
        external_names.append(full_name)
        text = str(i + 1) + ". " + full_name + " SCORE: " + str(result[i][1])
        external_scores.append(result[i][1])
        bot.send_message(chat_id=update.message.chat_id, text=text)

    plotting(external_names, external_scores, contest_number)
    bot.sendPhoto(chat_id=update.message.chat_id, photo=open('plot.png', 'rb'))