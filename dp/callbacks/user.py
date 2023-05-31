from aiogram import types
from loader import dp


@dp.callback_query_handler(text='hide')
async def ban_callback(callback: types.CallbackQuery):
    await callback.message.edit_text(text="Keys has been hide")