import uuid

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from markup_tool.models import Classification
from markup_tool.models import TelegramUser, Object, MarkingTask

bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton('Registration'))
    markup.add(KeyboardButton('Exit'))
    bot.send_message(message.chat.id, 'Please make a choice', reply_markup=markup)


def send_markup_task(message_id):
    obj = Object.objects.filter(marked=False).order_by('?').first()
    if obj:
        buttons = InlineKeyboardMarkup()
        btn_list = []
        all_classifications = Classification.objects.all()
        if all_classifications:
            for c in all_classifications:
                btn_list.append(InlineKeyboardButton(c.title, callback_data=f'classification: {c.id} object: {obj.id}'))
            buttons.add(*btn_list)
            with open(obj.image.path, 'rb') as obj_img:
                bot.send_photo(message_id, obj_img, reply_markup=buttons)
        else:
            bot.send_message(message_id, text='Administrator has not created classifications yet')
    else:
        bot.send_message(message_id, text='Unmarked objects not found')


@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text == 'Exit':
        bot.send_message(message.chat.id, 'Goodbye')
    elif message.text == 'Registration':
        if TelegramUser.objects.filter(telegram_user_id=message.from_user.id):
            msg_text = 'You are already registered'
        else:
            username = f'user-{uuid.uuid4().hex[:6]}'
            password = User.objects.make_random_password()
            user = User.objects.create_user(username=username, password=password)
            TelegramUser.objects.create(user=user, telegram_user_id=message.from_user.id)
            msg_text = f"""You have successfully registered\nYour username is: {username}\nYour password is: {password}"""
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton('Login'))
        bot.send_message(message.chat.id, msg_text, reply_markup=markup)
    elif message.text == 'Login':
        bot.send_message(message.chat.id,
                         'Please type your username and password. Example\nMy username is: user-9c000e\nMy password is: bLZGEsFZKS')
    elif message.text.startswith('My username is:'):
        credentials_list = message.text.split()
        if len(credentials_list) == 8:
            username = credentials_list[3]
            password = credentials_list[7]
            user = authenticate(username=username, password=password)
            telegram_user = TelegramUser.objects.filter(user=user, telegram_user_id=message.from_user.id)
            if telegram_user:
                markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                markup.add(KeyboardButton('My tasks'))
                markup.add(KeyboardButton('Exit'))
                bot.send_message(message.chat.id, 'Please make a choice', reply_markup=markup)
            else:
                bot.send_message(message.chat.id, 'login or password is incorrect')
        else:
            bot.send_message(message.chat.id,
                             'Please type your username and password strictly according to this format. Example:\nMy username is: user-9c000e\nMy password is: bLZGEsFZKS')
    elif message.text == 'My tasks':
        user = User.objects.filter(is_active=True, telegram_user__telegram_user_id=message.from_user.id)
        if user:
            send_markup_task(message.chat.id)
        else:
            bot.send_message(message.chat.id, 'You are not registered or deactivated')


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data.startswith('classification:'):
        data_list = call.data.split()
        classification = Classification.objects.get(id=data_list[1])
        obj = Object.objects.get(id=data_list[3])
        user = User.objects.get(telegram_user__telegram_user_id=call.from_user.id)
        if not obj.marked:
            MarkingTask.objects.create(user=user, classification=classification, object=obj)
        else:
            bot.send_message(call.message.chat.id, text='Object already marked. Please mark next object')
        send_markup_task(call.message.chat.id)


if __name__ == '__main__':
    bot.infinity_polling()
