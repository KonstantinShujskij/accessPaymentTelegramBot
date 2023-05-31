from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from dp.callbacks.objects import access as Callback
from templates import MessageData


get_access_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Get Access'))
refresh_access_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Refresh Access'))


def ban(user_id):
    text = f"Пользователь Заблокирован\n" \
           f"id: {user_id}\n" \

    keyboard = InlineKeyboardMarkup(row_width=2)

    allow_callback = Callback.new(action="clear", id=user_id)
    keyboard.add(InlineKeyboardButton('Разблокировать пользователя', callback_data=allow_callback))

    return MessageData(text, keyboard).__dict__


def clear(user_id):
    text = f"Пользователь Разблокирован\n" \
           f"id: {user_id}\n" \

    return MessageData(text).__dict__
