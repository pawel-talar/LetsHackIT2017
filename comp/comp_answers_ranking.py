import json
from db.comp import answers_ranking
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from pylab import savefig


plot_filename = 'plot.png'


def plotting(contest_number, highscores):
    y_pos = range(len(highscores))

    plt.bar(y_pos, [v for _, v in highscores], align='center')
    plt.xticks(y_pos, [k for (k, _) in highscores])
    plt.yticks(range(max([v for (_, v) in highscores]) + 1))

    plt.xlabel('Imię i nazwisko')
    plt.ylabel('Punkty')
    plt.title('Wyniki {} konkursu'.format(contest_number))

    savefig(plot_filename, bbox_inches = 'tight')


def contest_exists():
    return True


def get_tasks_per_user(answers_rank):
    tasks_per_user = {}
    for e in answers_rank:
        each = json.loads(e.decode())
        if not each['user_id'] in tasks_per_user:
            tasks_per_user[each['user_id']] = set([each['task_id']])
        else:
            tasks_per_user[each['user_id']].add(each['task_id'])
    return tasks_per_user


def answers_ranking_parse(redis_client, bot, update):
    assert len(update.message.text.split()) > 1
    assert update.message.text.split()[1].isdigit()

    contest_id = int(update.message.text.split()[1])
    tasks_per_user = get_tasks_per_user(answers_ranking(redis_client, contest_id))
    print(tasks_per_user)

    if not contest_exists():
        bot.send_message(chat_id=update.message.chat_id, text="Nie istnieje konkurs o podanym numerze")
        return

    show_user = lambda x: '{} {}'.format(x['first_name'], x['last_name'])
    highscores = sorted([(show_user(bot.get_chat(id)), len(v))
                for id, v in tasks_per_user.items()], key=lambda x: -x[1])[:5]

    highscores_text = '\n'.join(["{}, score: {}".format(id, score)
                              for (id, score) in highscores])
    bot.send_message(chat_id=update.message.chat_id, text=highscores_text)

    plotting(contest_id, highscores)
    bot.sendPhoto(chat_id=update.message.chat_id, photo=open(plot_filename, 'rb'))