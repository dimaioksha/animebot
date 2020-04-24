
import pandas as pd
from mongodb import mdb, search_or_save_user, update_user
data = pd.read_csv('omg.csv')
WANT_TO_KNOW_FOTO = True
def most_similar(number, data=data, the_most=True):
    try:
        similarity = data[str(number)].sort_values(ascending=False)[1:10]
        if the_most:
            return similarity.index[0]
    except Exception as e:
        return 0

def step_most_similar(message):
    try:
        user = search_or_save_user(mdb, message.from_user, message)
        user['selected_photo'] = int(message.text)
        result = most_similar(int(message.text), data)
        user['the_most_similar_photo'] = int(result)
        update_user(mdb, user)
    except Exception as e:
        pass
    # bot.send_message(message.chat.id, 'IDшник самой похожей фотки: <b>{1}</b>'.format(result))
    # print(result)