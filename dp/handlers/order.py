from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from templates import report_message
import bd
from utils import end_dialog
from states.admin.states import report_state


@dp.message_handler(text='/orders')
async def get_orders(message: types.message, state: FSMContext):
    user_id = message.chat.id

    try:
        partner = bd.get_partner(user_id)
    except Exception as error:
        return await end_dialog(message, str(error))

    if not partner or not partner.status == 'allow':
        return await end_dialog(message, "У вас нет доступа")

    await report_state.partner.set()
    await state.update_data(id=partner.api_id)
    await report_state.start_date.set()

    await message.answer(**report_message.get_start_date())
    await message.delete()

