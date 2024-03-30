from aiogram import F, types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

# from sqlalchemy.ext.asyncio import AsyncSession
# from aiogram.utils.formatting import as_list, as_marked_section, Bold

from database.orm_query import (
    orm_add_to_cart,
    orm_add_user,
)

from filters.chat_types import ChatTypeFilter
from handlers.menu_processing import get_menu_content
from kbds.inline import get_callback_btns

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession):
    media, reply_markup = await get_menu_content(session, level=0, menu_name="main")
    await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)

    # await message.answer("Привет, я виртуальный помощник",
    #                      reply_markup=get_callback_btns(btns={
    #                          'Нажми меня': 'some_1'
    #                      }))


# @user_private_router.callback_query(F.data.startswith('some_'))
# async def counter(callback: types.CallbackQuery):
#     number = int(callback.data.split('_')[-1])
#
#     await callback.message.edit_text(
#         text=f"Нажатий - {number}",
#         reply_markup=get_callback_btns(btns={
#             'Нажми еще раз': f'some_{number + 1}'
#         }))
