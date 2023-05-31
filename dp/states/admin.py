from aiogram.dispatcher import FSMContext
from aiogram import types

from states.admin.states import allow_access_state
from loader import dp
from api.requests.admin import create_access
from templates import access_messages, user_message
import bd
from utils import end_dialog


@dp.message_handler(state=allow_access_state.name)
async def set_name(message: types.Message, state: FSMContext):
    name = message.text

    await state.update_data(name=name)
    await allow_access_state.course.set()

    await message.answer(text='Курс:')


@dp.message_handler(state=allow_access_state.course)
async def set_course(message: types.Message, state: FSMContext):
    try:
        course = float(message.text)
    except Exception as error:
        return await end_dialog(message, str(error))

    await state.update_data(course=course)
    await allow_access_state.min.set()

    await message.answer(text='Минимальная сумма вывода:')


@dp.message_handler(state=allow_access_state.min)
async def set_min_value(message: types.Message, state: FSMContext):
    try:
        min_value = float(message.text)
    except Exception as error:
        return await end_dialog(message, str(error))

    await state.update_data(min_value=min_value)
    await allow_access_state.max.set()

    await message.answer(text='Максимальная сумма вывода:')


@dp.message_handler(state=allow_access_state.max)
async def set_max_value(message: types.Message, state: FSMContext):
    partner_id = (await state.get_data('telegram'))['id']
    name = str((await state.get_data('name'))['name'])
    course = str((await state.get_data('course'))['course'])
    min_value = str((await state.get_data('min'))['min_value'])

    await state.finish()

    try:
        max_value = str(float(message.text))

        access = create_access(name, course, min_value, max_value)
        bd.allow_partner(partner_id, access.id)

    except Exception as error:
        return await end_dialog(message, str(error))

    await dp.bot.send_message(chat_id=partner_id, text='Вам был одобрен доступ!',
                              reply_markup=user_message.refresh_access_keyboard)
    await dp.bot.send_message(chat_id=partner_id, **access_messages.data(access))

    await message.answer(text='success')