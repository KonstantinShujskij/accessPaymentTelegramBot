from aiogram import types

from loader import dp
import bd
from templates import user_message
from utils import end_dialog


@dp.message_handler(text='/start')
async def command_start(message: types.message):
    user_id = message.from_user.id

    try:
        partner = bd.get_partner(user_id)
    except Exception as error:
        return await end_dialog(message, str(error))


    if not partner:
        await message.answer(text="Бот запущен", reply_markup=user_message.get_access_keyboard)
        return await message.delete()

    if partner.status == 'allow':
        await message.answer(text="Бот запущен", reply_markup=user_message.refresh_access_keyboard)
        return await message.delete()

    if partner.status == 'check':
        return await end_dialog(message, "Ваш запрос на модерации")

    if partner.status == 'ban':
        return await end_dialog(message, "Вы заблокированы!")


