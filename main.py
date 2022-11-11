import telebot, json, datetime

bot_start = datetime.datetime.now().timestamp()

bot = telebot.TeleBot(open('token.txt', encoding='utf-8').read())

def config_open():
    global database
    with open('chats.json', encoding='utf-8') as f:
        database = json.load(f)

def config_save():
    global database
    with open('chats.json', 'w', encoding="utf-8") as f:
        json.dump(database, f, indent=4, ensure_ascii=False)


@bot.message_handler(content_types=['text'])
def messager(message):

    config_open()
    if message.chat.id not in database:
        database.append(message.chat.id)
        bot.send_message(message.chat.id, f"✅ Теперь этот чат подключен к глобальному чату!")
        config_save()

    config_open()
    if message.date >= bot_start:
        if message.chat.type == "private": #ЛС
            if message.reply_to_message == None:
                print(f"\n[{message.from_user.first_name}] @{message.from_user.username}:\n{message.text}\n")
                for i in database:
                    bot.send_message(i, f"[{message.from_user.first_name}] @{message.from_user.username}:\n{message.text}")
        
        else: #ГРУППА, СУПЕРГРУППА, КАНАЛ
            if message.reply_to_message == None:
                print(f"\n[{message.chat.title}] @{message.from_user.username}:\n{message.text}\n")
                for i in database:
                    if i != message.chat.id:
                        bot.send_message(i, f"[{message.chat.title}] @{message.from_user.username}:\n{message.text}")    
    else:
        return #ЕСЛИ СООБЩЕНИЕ БЫЛО ПОЛУЧЕНО ДО ЗАПУСКА БОТА!

while True:
    print(".")
    try:
        print("[bot starting!]\n")
        bot.remove_webhook()
        bot.polling(none_stop=True)
    except Exception as err:
        print("[bot stoping!]\n")
        print(f"Error: {err}\n")