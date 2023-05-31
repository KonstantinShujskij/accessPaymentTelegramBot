from aiogram import types
from aiogram.dispatcher import FSMContext

import check
from loader import dp
from dp.callbacks.objects import access as Callback
from states.admin.states import allow_access_state
from api.requests.admin import refresh_access
import bd
from templates import access_messages, user_message
from utils import end_dialog


@dp.callback_query_handler(Callback.filter(action='ban'))
async def ban_callback(callback: types.CallbackQuery, callback_data: dict):
    user_id = callback.from_user.id
    partner_id = callback_data['id']

    try:
        check.is_admin(user_id)
        bd.ban_partner(partner_id)
    except Exception as error:
        return await end_dialog(callback.message, str(error))

    await dp.bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await dp.bot.send_message(chat_id=user_id, **user_message.ban(partner_id))

    await dp.bot.send_message(chat_id=partner_id, text='Вы заблокированы!',
                              reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler(Callback.filter(action='allow'))
async def ban_callback(callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    user_id = callback.from_user.id
    partner_id = callback_data['id']

    try:
        check.is_admin(user_id)
    except Exception as error:
        return await end_dialog(callback.message, str(error))

    await allow_access_state.telegram.set()
    await state.update_data(id=partner_id)
    await allow_access_state.name.set()

    await dp.bot.send_message(chat_id=user_id, text='Имя:')


@dp.callback_query_handler(Callback.filter(action='refresh'))
async def ban_callback(callback: types.CallbackQuery, callback_data: dict):
    user_id = callback.from_user.id
    partner_id = callback_data['id']

    try:
        check.is_admin(user_id)

        partner = bd.get_partner(partner_id)
        access = refresh_access(partner.api_id)

        bd.refresh_partner(partner_id)
    except Exception as error:
        return await end_dialog(callback.message, str(error))

    await dp.bot.send_message(chat_id=partner_id, text='Ваш доступ обновлен!',
                              reply_markup=user_message.refresh_access_keyboard)

    await dp.bot.send_message(chat_id=partner_id, **access_messages.data(access))

    await dp.bot.send_message(chat_id=user_id, text='success')


@dp.callback_query_handler(Callback.filter(action='clear'))
async def ban_callback(callback: types.CallbackQuery, callback_data: dict):
    user_id = callback.from_user.id
    partner_id = callback_data['id']

    try:
        check.is_admin(user_id)

        partner = bd.get_partner(partner_id)
    except Exception as error:
        return await end_dialog(callback.message, str(error))

    if partner.api_id == 'undefined':
        try:
            bd.clear_partner(partner_id)
        except Exception as error:
            return await end_dialog(callback.message, str(error))

        await dp.bot.send_message(chat_id=partner_id, text='вы разблокированы!',
                                  reply_markup=user_message.get_access_keyboard)

        await dp.bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await dp.bot.send_message(chat_id=user_id, **user_message.clear(partner_id))

    else:
        try:
            bd.reban_partner(partner_id)
        except Exception as error:
            return await end_dialog(callback.message, str(error))

        await dp.bot.send_message(chat_id=partner_id, text='вы разблокированы!',
                                  reply_markup=user_message.refresh_access_keyboard)

        await dp.bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await dp.bot.send_message(chat_id=user_id, **user_message.clear(partner_id))