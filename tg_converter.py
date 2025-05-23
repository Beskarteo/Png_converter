pip install -r requirements.txt

token = '' # уникальный токен бота

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['help'])
def prin_t(message):
    bot.send_message(message.chat.id, '/start - старт бота \n/convert - конвертировать фото \n/help - существующие команды')

@bot.message_handler(commands=['start'])
def menu(message):
    keyboard = types.ReplyKeyboardMarkup(True, True)
    keyboard.add('/convert')
    keyboard.add('/help')
    send = bot.send_message(message.chat.id, f'Здравствуйте, {message.chat.first_name}',reply_markup=keyboard)
    bot.send_message(message.chat.id, 'Для конвертации фото воспользуйтесь командой /convert и отправте фото')
    #bot.register_next_step_handler(message, add_user)

@bot.message_handler(commands=['convert'])
def menu(message):
    bot.register_next_step_handler(message, ask_razm)
    bot.send_message(message.chat.id, 'Для конвертации отправте фото (.jpg и как фото)')

def ask_razm(message):
    if message.photo == None:
        menu(message)
    else:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f"Import-image{message.from_user.id}.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
        vopr(message)

def vopr(message):
    keyboard = types.ReplyKeyboardMarkup(True, False)
    keyboard.add('Формат для стикеров')
    keyboard.add('Нет')
    send = bot.send_message(message.chat.id, 'Нужно ли вам изменять размер фото',reply_markup=keyboard)
    bot.register_next_step_handler(message, re_size)

def re_size(message):
    if str(message.text) != 'Формат для стикеров' and str(message.text) != 'Нет':
        bot.send_message(message.chat.id, 'Отправьте Да или Нет')
        vopr(message)
    if message.text == 'Формат для стикеров':
        sp_sz = [512, 512]      #vibor_rasm(message)
    if message.text == 'Нет':
        sp_sz = []
    converter(message, sp_sz)

#def vibor_rasm(message):
#    keyboard = types.ReplyKeyboardMarkup(True, False)
#    keyboard.add('512x512')
#    #keyboard.add('Нет')
#    send = bot.send_message(message.chat.id, 'Выберите нужный размер',reply_markup=keyboard)
#    print(message.text)
#    return message.text

def converter(message, sp_sz):
    img = Image.open(f"Import-image{message.from_user.id}.jpg")
    rgb_im = img.convert('RGB')
    #
    if sp_sz != []:
        rgb_im = img.resize(tuple(sp_sz))   #re_size(message.caption)
    #
    rgb_im.save(f'new_img{message.from_user.id}.png', format='PNG', quality=100, optimize=True, dpi=(300, 300)) #обрезка фото
    with open(f"new_img{message.from_user.id}.png", "rb") as file:
        bot.send_document(message.chat.id, document=file)
        os.remove(f"new_img{message.from_user.id}.png")
    #
    with open(f"Import-image{message.from_user.id}.jpg", "rb") as file:
        os.remove(f"Import-image{message.from_user.id}.jpg")
    #
    print(message.chat.username)
    print(message.chat.first_name)


if __name__ == '__main__':
    bot.infinity_polling()
