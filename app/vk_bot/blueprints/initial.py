from vkbottle.bot import Blueprint, Message

from app.backend.handlers.users.schemes import UserSchema
from app.vk_bot.keyboards.change_group import change_group_keyboard
from app.vk_bot.keyboards.menu import menu_keyboard
from app.vk_bot.rules.contains_trigger import ContainsTriggerRule
from config import settings

blueprint = Blueprint()

MENU_TRIGGERS = [
    'меню',
    'в меню',
    'главное меню',
    'начать',
    'покежь клаву',
    'клава',
    'start',
    'старт',
    'привет',
    'расписание',
]


@blueprint.on.message(ContainsTriggerRule(triggers=MENU_TRIGGERS, payload_triggers=['main menu']))
async def hello_handler(message: Message = None, user: UserSchema = None):
    new_user = user.group_index is None

    if new_user:
        answer_message = (
            'Привет! Для начала работы с ботом тебе нужно написать "Старт" или "Начать", '
            'а потом тебе нужно поменять свою группу через настройки.'
            '\n\nСписок команд:'
            '\n vk.com/@mpsu_schedule-vse-komandy-bota'
        )
        await message.answer(answer_message, keyboard=change_group_keyboard)

    await message.answer(message=settings.VK_EMPTY_MESSAGE, keyboard=menu_keyboard)
