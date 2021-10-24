# ... Сообщения ...
DEFAULT_ANSWER_MESSAGE = 'Oк'
TROUBLESHOOT = 'Попробуй написать "Старт" чтобы открыть меню, ' \
               'а потом зайти в "Настройки"'

COMMANDS_LIST = 'https://vk.com/wall-206763355_30' \
                '\nhttps://vk.com/wall-206763355_42' \

GREETINGS = 'Привет! Для начала работы с ботом тебе нужно написать "Старт" или "Начать", ' \
            'а потом тебе нужно поменять свою группу через настройки.' \
            '\n\nСписок команд:' \
            '\n' + COMMANDS_LIST \
          + '\n\nЛЮБОЕ СООБЩЕНИЕ-НЕ-КОМАНДУ БОТ  БУДЕТ ВОСПРИНИМАТЬ, КАК ПОПЫТКУ С НИМ ПОБОЛТАТЬ!!'

CHANGE_GROUP_MESSAGE = 'Напиши мне новый номер группы' \
                       '\n\nЕсли вы в беседе, перед номером напишите "бот", например "бот 218"'

INVALID_INPUT_MESSAGE = "Мне нужны только циферки!"

INVALID_COMMAND = 'Если ты пытаешься получить расписание, а я отвечаю какую-то фигню, отключи' \
                  'виртуального собеседника' \
                  '\n\n Список команд:' \
                  '\n' + COMMANDS_LIST \
                + '\n\n' + TROUBLESHOOT

WRONG_COMMUNITY = 'Если ты пытаешься со мной поболтать, то в этой группе у тебя не получится :(' \
                  '\nМне отключили интеллект, потому что я "слишком грубый" 😢' \
                  '\n\nЕсли хочешь поболтать, я свободен в группе:' \
                  '\nhttps://vk.com/mpsu_schedule' \
                  '\n\nЧто-то не работает?' \
                  '\n' + TROUBLESHOOT

AI_FRIEND = "Виртуальный собеседник "


# ... Переменные ...

current_spreadsheet = {
    "id": None,
    "updated_time": ""
}


# ... Кастомные сообщения ...


def Settings(group_index):
    return f"""Твоя/ваша группа: {group_index}

Список команд:
https://vk.com/mpsu_schedule?w=wall-206763355_30
https://vk.com/wall-206763355_42


F.A.Q:
https://vk.com/topic-206763355_48153565

Если чё-то не работает, пиши мне @baboomka"""


def Spreadsheet_update_info():
    return f"Расписание последний раз обновлялось сегодня в {current_spreadsheet['updated_time']}" \
           f"\n\nid: {current_spreadsheet['id']}"
