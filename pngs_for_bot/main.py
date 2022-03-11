import telebot
import time
from termcolor import cprint
import os

directory = os.path.abspath(__file__)
search = list(filter(lambda x: x.endswith('.png'), os.listdir(directory)))[::-1]
print(search)

bot = telebot.TeleBot('1497320712:AAG5IgljuHXtJ9vhbtwPGMYwHLChwACvoKM')
for_help = "\n".join(list(map(lambda x: "  ●" + x[:-4], search)))

history = []


@bot.message_handler(commands=["start", "hello", "hi"])
def start(message):
    bot.send_message(message.chat.id, f"""Привет {message.from_user.first_name},
я телеграмм бот для закрепления знаний по геометрии!
Напиши /search <Определение или название теоремы> или /help для получения помощи!""")
    print(f"<{message.from_user.first_name} {message.from_user.last_name} [{message.from_user.id}]>: {message.text}")


@bot.message_handler(commands=['search'])
def send_file(message):
    global history, search
    start_ = time.time()
    msg = str(message.text).split()
    if len(msg) == 1:
        bot.send_message(message.chat.id, "Вы не указали то, что хотите искать.")
        return None
    else:
        arg = list(filter(lambda x: x is not None, [msg[1] if len(msg) < 3 else msg[1] + ' ' + msg[2]]))[0]
    temp = list(filter(lambda x: arg.lower() in x.lower(), search))
    if any(temp):
        bot.send_document(message.chat.id, open(str(list(temp)[0]), 'rb'))
    else:
        bot.send_message(message.chat.id, "Извините, но файл не найден.")
    print(f"<{message.from_user.first_name} {message.from_user.last_name} [{message.from_user.id}]>: {message.text}")
    end_ = time.time()
    print("Время ответа:", end_ - start_)
    history.append(end_ - start_)
    print("Среднее время ответа:", sum(history) / len(history))
    if sum(history) / len(history) > 1.5:
        cprint(f"Слишком большое время ответа", on_color='on_red', color="grey")


@bot.message_handler(commands=["help"])
def help_for_user(message):
    bot.send_message(message.chat.id, f"""Вот что я знаю (Но я ещё учусь:) ):\n{for_help}""")
    bot.send_message(message.chat.id, "Напиши /search <Определение или название теоремы>")
    print(f"<{message.from_user.first_name} {message.from_user.last_name} [{message.from_user.id}]>: {message.text}")


# @bot.message_handler(content_types=['text', 'document', 'audio'])
# def not_understand(message):
#     bot.send_message(message.chat.id, f"Я не знаю такой команды: '{message.text}'")
#     print(f"<{message.from_user.first_name} {message.from_user.last_name} [{message.from_user.id}]>: {message.text}")

@bot.message_handler(content_types=['text', 'document', 'audio'])
def greet(message):
    if "." in message.text.lower():
        bot.send_message(message.chat.id, """С днем рожденья, папа!
Долгих-долгих лет.
Пусть приходит радость
В каждый твой рассвет.

Дни пусть золотые
Не спеша идут.
Денежки шальные
На счетах растут.

Пусть удача знает,
Где тебя искать.
Всё, что пожелаешь,
Будет исполнять.

Здоровье будет крепким,
А сердце — молодым,
Душа по-детски светлой.
Ты будь судьбой храним!

""")


bot.infinity_polling()
