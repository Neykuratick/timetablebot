import traceback

from aiogram import F
from aiogram import Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from app.backend.db.models.action import ButtonsEnum
from app.frontend.clients.telegram import TelegramClient
from app.frontend.dto.enum import SourcesEnum
from app.frontend.dto.user import User
from app.frontend.singletons import Clients
from app.frontend.tg_bot.keyboards.feedback import get_empty_feedback_keyboard
from app.frontend.tg_bot.keyboards.menu import get_detailed_menu
from app.frontend.tg_bot.keyboards.menu import get_menu_keyboard
from app.frontend.tg_bot.keyboards.settings import get_change_group_keyboard
from app.frontend.tg_bot.misc.callbacks import Callback
from app.frontend.tg_bot.misc.callbacks import CallbackActions
from app.frontend.tg_bot.misc.states import FSMStates
from app.frontend.vk_bot.misc.request_clients import RequestClients
from config import settings

initial_router = Router()


@initial_router.message(commands=["start"])
@initial_router.callback_query(Callback.filter(F.action.in_({CallbackActions.menu})))
async def hello_handler(
    message: Message | CallbackQuery,
    current_user: User,
    state: FSMContext,
) -> None:
    if isinstance(message, CallbackQuery):
        await message.answer(settings.TELEGRAM_EMPTY_MESSAGE)

    new_user = current_user.group_number is None
    await RequestClients.backend.mark_action(
        source=SourcesEnum.telegram,
        user_id=current_user.id,
        button_name=ButtonsEnum.menu,
    )
    try:
        if await state.get_state():
            await state.clear()
    except KeyError:
        traceback.print_exc()

    if new_user:
        answer_message = (
            'Привет! Для начала работы с ботом тебе нужно написать "/start", '
            "а потом тебе нужно поменять свою группу через настройки. \n\n"
            "Либо просто нажми на кнопку 👇 внизу 👇"
        )
        reply_markup = get_change_group_keyboard()
    else:
        answer_message = "Выбери нужное действие"
        reply_markup = get_menu_keyboard()

    await TelegramClient.send_message(
        query=message,
        text=answer_message,
        reply_markup=reply_markup,
    )


@initial_router.callback_query(Callback.filter(F.action.in_({CallbackActions.suicide})))
async def delete_message(query: CallbackQuery) -> None:
    await TelegramClient.bot.delete_message(
        message_id=query.message.message_id,
        chat_id=query.from_user.id,
    )
    await query.answer(settings.TELEGRAM_EMPTY_MESSAGE)


@initial_router.callback_query(Callback.filter(F.action.in_({CallbackActions.pattern_search})))
async def pattern_search(query: CallbackQuery, current_user: User, state: FSMContext) -> None:
    greeting = (
        "Добро пожаловать в поиск по шаблону. В этом разделе можно найти все пары, "
        "в названии которых содержится твой запрос (шаблон) \n\n"
        "Например, если ты напишешь имя (или часть имени) преподавателя, то бот отправит тебе его "
        "расписание\n\n"
        "👇 Напиши что ты хочешь найти в расписании"
    )

    await query.answer(settings.TELEGRAM_EMPTY_MESSAGE)

    await Clients.telegram.send_message(
        query=query,
        text=greeting,
        reply_markup=get_empty_feedback_keyboard(
            back=CallbackActions.detailed,
        ),
    )

    await state.set_state(state=FSMStates.pattern_input)
    await RequestClients.backend.mark_action(
        user_id=current_user.id,
        button_name=ButtonsEnum.pattern_mode,
    )


@initial_router.callback_query(Callback.filter(F.action.in_({CallbackActions.detailed})))
async def detailed_search(query: CallbackQuery, current_user: User, state: FSMContext) -> None:
    """Отправляет клавиатуру с выбором недели и паттерн поиском"""
    data = await state.get_data()
    pattern = data.get("pattern")
    if not pattern:
        await state.clear()

    if pattern:
        keyboard = get_detailed_menu(pattern=pattern)
        header = f'⚠️ Сейчас включён режим поиска по этому шаблону: "{pattern}"'
    else:
        keyboard = get_detailed_menu()
        header = "Выбери действие"

    await query.answer(settings.TELEGRAM_EMPTY_MESSAGE)

    await TelegramClient.send_message(
        query=query,
        text=header,
        reply_markup=keyboard,
    )

    await RequestClients.backend.mark_action(
        source=SourcesEnum.telegram,
        user_id=current_user.id,
        button_name=ButtonsEnum.detailed_search,
    )


@initial_router.callback_query(Callback.filter(F.action.in_({CallbackActions.stop_pattern_search})))
async def stop_search_pattern(query: CallbackQuery, current_user: User, state: FSMContext) -> None:
    await state.clear()
    await query.answer(settings.TELEGRAM_EMPTY_MESSAGE)
    keyboard = get_detailed_menu()

    await TelegramClient.send_message(
        query=query,
        text="Режим поиска сброшен",
        reply_markup=keyboard,
    )

    await RequestClients.backend.mark_action(
        source=SourcesEnum.telegram,
        user_id=current_user.id,
        button_name=ButtonsEnum.detailed_search,
    )
