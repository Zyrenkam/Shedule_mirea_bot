import telebot
from telebot import types

from determinate_fill import *
from find_shedule import *
from parser_excel import *

token = ''
bot = telebot.TeleBot(token)

full_info = {'institute': '-', 'kurs': '-', 'group': '-'}

rus_ekv_day = {'mon': 'ПОНЕДЕЛЬНИК', 'tue': 'ВТОРНИК', 'wed': 'СРЕДА', 'thu': 'ЧЕТВЕРГ', 'fri': 'ПЯТНИЦА', 'sat': 'СУББОТА'}
rus_ekv_inst = {'IIT': 'ИИТ', 'III': 'ИИИ', 'IPTIP': 'ИПТИП', 'IRI': 'ИРИ',
                'RASPISANIE': 'КПК', 'ITKHT': 'ИТХТ', 'IKB': 'ИКБ', 'ITU': 'ИТУ'}

kb = types.InlineKeyboardMarkup(row_width=6)
kb_mon = types.InlineKeyboardButton(text='Пн', callback_data='mon')
kb_tue = types.InlineKeyboardButton(text='Вт', callback_data='tue')
kb_wed = types.InlineKeyboardButton(text='Ср', callback_data='wed')
kb_thu = types.InlineKeyboardButton(text='Чт', callback_data='thu')
kb_fri = types.InlineKeyboardButton(text='Пт', callback_data='fri')
kb_sat = types.InlineKeyboardButton(text='Сб', callback_data='sat')
kb.add(kb_mon, kb_tue, kb_wed, kb_thu, kb_fri, kb_sat)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Привет! Я - ваш личный помощник.'
                          ' Напиши номер своей группы с тире, чтобы получить расписание. \nНапример, ЭСБО-01-22')
    print(message.text)


@bot.message_handler(func=lambda message: True)
def processing(message):
    global posible_files
    print(message.from_user)
    text = message.text
    group_number = determinate_group(text)
    # при правильном наборе группы условие выполняется, тк функция добавляет тире в текст
    if '-' in group_number:
        bot.reply_to(message, f'Сейчас найдем группу {group_number}.')
        print('+', group_number)
        data_fill(group_number, full_info)
        bot.send_message(message.chat.id, f'Институт: {rus_ekv_inst[full_info["institute"]]}'
                                          f' \nКурс: {full_info["kurs"]}'
                                          f' \nГруппа: {full_info["group"]}', reply_markup=kb)
        print(full_info)
        posible_files = parse_shedules(full_info)
        print(posible_files)
    else:
        bot.reply_to(message, f'Ошибка в написании группы {determinate_group(text)}')
        print('-', group_number, ': ', text)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    ready_shed = shedule(posible_files, full_info)
    date = datetime.datetime.now()
    week_number_num = date.isocalendar().week

    if week_number_num % 2 != 0:
        print(ready_shed)
        ready_shed = ready_shed[1]
    else:
        ready_shed = ready_shed[0]

    print('======')
    print(ready_shed[call.data])
    print('======')

    msg_to_send = str(rus_ekv_day[call.data]) + '\n'
    for i in range(0, len(ready_shed[call.data])):
        msg_to_send += str(i+1) + 'пара: '
        msg_to_send += ready_shed[call.data][i][0] + ' ' + ready_shed[call.data][i][1] + ' ' + ready_shed[call.data][i][3]
        msg_to_send += '\n'

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg_to_send,
                          reply_markup=kb)


try:
    bot.polling(none_stop=True)

except KeyboardInterrupt:
    exit()
