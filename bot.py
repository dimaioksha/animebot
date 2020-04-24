import telebot
import config
from telebot import types
import random
from mongodb import mdb, search_or_save_user, update_user
import time
from encoder import getting_encoder
import numpy as np
from numpy import load
import pandas as pd
from pictures import data, most_similar, step_most_similar
from sklearn.metrics.pairwise import cosine_similarity
from io import BytesIO
from scipy import misc
from PIL import Image
from keras import backend as K

bot = telebot.TeleBot(config.TOKEN)
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_chat_action(message.chat.id, 'typing')
    user = search_or_save_user(mdb, message.from_user, message)
    print(user)
    sti = open(r'C:\Users\Dmitry\Desktop\AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)
    #keyboard

    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    item1 = types.KeyboardButton('Рандомное число')
    item2 = types.KeyboardButton('Как дела?')
    item3 = types.KeyboardButton('Самая похожая фотография')
    # markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup1.add(item1, item2, item3)
    # markup2.add(item3)
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы быть подопытным кроликом.".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup1)
# @bot.message_handler(commands=['chose'])
# def select_picture(message):
@bot.message_handler(commands=['select_photo', 'photo'])
def find_photo(message):
    message.text = 'Самая похожая фотография'
    hello_world(message)
@bot.message_handler(func=lambda message: message.caption == '/upload_photo', content_types=['photo'])
def upload_photo(message):
    K.clear_session()
    # updates = bot.get_updates()
    bot.send_message(message.chat.id, '__Ваше фото обрабатывается . . .__', parse_mode="Markdown")
    # print([u.message.photo for u in updates if u.message.photo])
    file = bot.get_file(message.photo[-1].file_id)
    file = bot.download_file(file.file_path)
    file = BytesIO(file)
    # file = misc.imread(BytesIO(file))
    file = Image.open(file)
    new_width = 64
    new_height = 64
    file = file.resize((new_width, new_height), Image.ANTIALIAS)
    encoder = getting_encoder()
    vector = encoder.predict(np.array(file).reshape(1, 64, 64, 3))
    encodings = load('encodings.npy')
    similarity = cosine_similarity(encodings.reshape(len(encodings), 256), vector.reshape(1, 256))
    ids = similarity.argmax()
    K.clear_session()
    bot.send_message(message.chat.id, 'Почти готово . . .', parse_mode='Markdown')
    DIR = r'C:/Users/Dmitry/PycharmProjects/telegrambots/first_bot/data/' + str(ids) + '.png'
    anime_image = Image.open(DIR)
    new_width = 512
    new_height = 512
    anime_image.resize((new_width, new_height), Image.ANTIALIAS)

    #bot.send_photo(chat_id=message.chat.id, photo=Image.open(BytesIO(an    ime_image)), caption='Готово!')
    bot.send_photo(chat_id=message.chat.id, photo=open(DIR, 'rb'), caption='Готово!')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, ' Найти похожее фото из базы данных фото: /photo \n Загрузить свое фото и найти похожее на него: /upload_photo \n Для сверхразумов: /start')
@bot.message_handler(commands=['upload_photo'])
def invalid_upload_photo(message):
    bot.send_message(message.chat.id, 'Если вы хотите загрузить свою фотграфию, загрузите ее в диалог с ботом и добавьте описание\n"/upload_photo" без кавычек')

@bot.message_handler(content_types=['text'])
def hello_world(message):
    bot.send_chat_action(message.chat.id, 'typing')
    # want_to_know_photo = True
    if message.chat.type == 'private':
        if message.text == 'Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0,100)))
        elif message.text == 'Как дела?':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('Хорошо', callback_data='good')
            item2 = types.InlineKeyboardButton('Не очень', callback_data='bad')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'У меня дела отлично. А у тебя как?', reply_markup=markup)
        elif message.text == 'Привет' or message.text == 'привет':
            user = search_or_save_user(mdb, message.from_user, message)
            if user['first_time'] == True:
                welcome(message)
                user['first_time'] = False
                update_user(mdb, user)
            else:
                bot.send_message(message.chat.id, 'Привет! Ознакомиться с командами можно написав /help')
        elif message.text == 'Самая похожая фотография':
            try:
                 markup = types.ForceReply(selective=False)
                 replied = bot.send_message(message.chat.id, "Введите номер картинки, для которой вы хотите найти самую похожую фотографию:\n", reply_markup=markup)
                 timing = time.time()
                 bot.register_next_step_handler(replied, step_most_similar)
                 time.sleep(5)
                 user = search_or_save_user(mdb, message.from_user, message)
                 bot.send_message(message.chat.id, 'Выбранная фотография:')
                 DIR_SEL = r'C:/Users/Dmitry/PycharmProjects/telegrambots/first_bot/data/' + str(user['selected_photo']) + '.png'
                 DIR_SIM = r'C:/Users/Dmitry/PycharmProjects/telegrambots/first_bot/data/' + str(user['the_most_similar_photo']) + '.png'
                 bot.send_photo(chat_id=message.chat.id, photo=open(DIR_SEL, 'rb'))
                 while(user['the_most_similar_photo'] == None):
                     user = search_or_save_user(mdb, message.from_user, message)
                     if time.time() - timing > 20.0:
                         bot.send_message(message.chat.id, 'Время ожидания истекло!')
                 if user['the_most_similar_photo'] != None:
                     bot.send_message(message.chat.id, 'IDшник самой похожей на вашу фотографию: {0}'.format(user['the_most_similar_photo']))
                 bot.send_photo(message.chat.id, photo=open(DIR_SIM, 'rb'))
            except Exception as e:
                bot.send_message(message.chat.id, 'ERROR with finding photo')
        else:
            bot.send_message(message.chat.id, 'Пока что я не научился отвечать на это =) Update soon.')
    # чтобы бот отправлял просто само сообщение: bot.send_message(message.chat.id, message.text)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и здорово')
                # remove inline buttons
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Ого, вот как!',
                                      reply_markup=None)
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает(')
                # remove inline buttons
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Жаль.',
                                           reply_markup=None)
                # sending alert
                bot.answer_callback_query(chat_id=call.message.chat.id, show_alert=True,
                                          text='now ure gay')
    except Exception as e:
        pass

bot.polling(none_stop=True)