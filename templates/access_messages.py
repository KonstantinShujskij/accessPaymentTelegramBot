from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dp.callbacks.objects import access as Callback
from templates import MessageData


def demand_access(user_id, user_name):
    text = f"Пользователь запрашивает доступ\n" \
           f"id: {user_id}\n" \
           f"user name: @{user_name}"

    keyboard = InlineKeyboardMarkup(row_width=2)

    ban_callback = Callback.new(action="ban", id=user_id)
    keyboard.add(InlineKeyboardButton('Запретить доступ', callback_data=ban_callback))

    allow_callback = Callback.new(action="allow", id=user_id)
    keyboard.add(InlineKeyboardButton('Разрешить доступ', callback_data=allow_callback))

    return MessageData(text, keyboard).__dict__


def refresh_access(user_id, user_name):
    text = f"Пользователь запрашивает обновление доступа\n" \
           f"id: {user_id}\n" \
           f"user name: @{user_name}"

    keyboard = InlineKeyboardMarkup(row_width=2)

    ban_callback = Callback.new(action="ban", id=user_id)
    keyboard.add(InlineKeyboardButton('Запретить доступ', callback_data=ban_callback))

    refresh_callback = Callback.new(action="refresh", id=user_id)
    keyboard.add(InlineKeyboardButton('Обновить доступ', callback_data=refresh_callback))

    return MessageData(text, keyboard).__dict__


def data(access):
    text = f'accessToken: <code>{access.accessToken}</code>\n' \
           f'privateToken: <code>{access.privateToken}</code>'

    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton('Скрыть', callback_data="hide"))

    return MessageData(text, keyboard).__dict__
