from vkbottle import Keyboard
from vkbottle import KeyboardButtonColor
from vkbottle import Text

menu_keyboard = Keyboard(one_time=False, inline=False)
menu_keyboard.add(Text("🔎 Сегодняшние пары", {"cmd": "today"}), KeyboardButtonColor.PRIMARY)
menu_keyboard.add(Text("🔎 Завтрашние пары", {"cmd": "tomorrow"}), KeyboardButtonColor.PRIMARY)
menu_keyboard.row()
menu_keyboard.add(Text("👀 Подробный поиск", {"cmd": "detailed"}), KeyboardButtonColor.SECONDARY)
menu_keyboard.row()
menu_keyboard.add(Text("🤖 ChatGPT", {"cmd": "chatgpt"}), KeyboardButtonColor.POSITIVE)
menu_keyboard.add(Text("🛠 Настройки", {"cmd": "settings"}), KeyboardButtonColor.SECONDARY)
menu_keyboard.row()
menu_keyboard.add(Text("Убрать клавиатуру", {"cmd": "suicide"}), KeyboardButtonColor.NEGATIVE)
