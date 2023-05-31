import time

from aiogram import types
from aiogram.dispatcher import FSMContext

from utils import parse_time, end_dialog
from loader import dp
from states.admin.states import report_state
from api.requests import admin
from templates import report_message
from excel import create_report


@dp.message_handler(state=report_state.start_date)
async def set_course(message: types.Message, state: FSMContext):
    value = message.text

    start_time = 0

    try:
        if not value.lower() == 'all':
            start_time = parse_time(value)
    except Exception as error:
        return await end_dialog(message, str(error))

    await state.update_data(value=start_time)
    await report_state.stop_date.set()

    await message.answer(**report_message.get_stop_date())


@dp.message_handler(state=report_state.stop_date)
async def set_course(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    value = message.text
    stop_time = int(time.time() * 1000)

    start_date = await state.get_data('start_date')
    start_time = start_date['value']

    partner = await state.get_data('partner')
    partner_id = partner['id']

    await state.finish()

    try:
        if not value.lower() == 'now':
            stop_time = parse_time(value)

        orders = admin.get_orders(start_time, stop_time, partner_id)
    except Exception as error:
        return await end_dialog(message, str(error))

    loader_message = await dp.bot.send_message(chat_id=user_id, text='Пожалуйста подождите')

    document = create_report(orders, 'report')

    await dp.bot.send_document(chat_id=user_id, document=document)
    await loader_message.delete()

