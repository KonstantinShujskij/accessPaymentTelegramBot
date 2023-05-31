from aiogram import types

from loader import dp
from data import config
from templates import access_messages
import bd
from utils import end_dialog


@dp.message_handler(text='Get Access')
async def get_access(message: types.message):
    user_id = message.chat.id
    user_name = message.from_user.username

    try:
        partner = bd.get_partner(user_id)
    except Exception as error:
        return await end_dialog(message, str(error))

    if not partner:
        try:
            bd.create_new_partner(user_id)
        except Exception as error:
            return await end_dialog(message, str(error))

        await dp.bot.send_message(chat_id=config.admin_id, **access_messages.demand_access(user_id, user_name))
        await message.answer(text="Ваш запрос на модерации", reply_markup=types.ReplyKeyboardRemove())
        await message.delete()

        return

    if partner.status == 'check':
        return await end_dialog(message, "Ваш запрос на модерации")

    if partner.status == 'ban':
        return await end_dialog(message, "Ва заблокированы!")

    if partner.status == 'allow':
        return await end_dialog(message, "У вас уже есть доступ!")


@dp.message_handler(text='Refresh Access')
async def refresh_access(message: types.message):
    user_id = message.chat.id
    user_name = message.from_user.username

    try:
        partner = bd.get_partner(user_id)
    except Exception as error:
        return await end_dialog(message, str(error))

    if not partner:
        return await end_dialog(message, "У вас нет доступа")

    if partner.status == 'check':
        return await end_dialog(message, "Ваш запрос на модерации")

    if partner.status == 'ban':
        return await end_dialog(message, "Вы заблокированы!")

    if partner.status == 'allow':
        try:
            bd.wait_partner(user_id)
        except Exception as error:
            return await end_dialog(message, str(error))

        await dp.bot.send_message(chat_id=config.admin_id, **access_messages.refresh_access(user_id, user_name))

        return await end_dialog(message, "Ваш запрос на модерации")




