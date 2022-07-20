import logging  # для ведения логов
import telegram as tg
import telegram.ext
import os
import re as r
from dotenv import load_dotenv
from gauges import gauges_db

logging.basicConfig(  # для ведения логов (оф. документация)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

updater = tg.ext.Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update: tg.Update, context: tg.ext.CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Введите код КН-24")


def decode_station(i):  #проверяем наличие станции в базе данных
    code = i.split()[0]
    if code in gauges_db.keys():
        return f'{gauges_db[code]}'
    else:
        return '<нет такой станции>'


def date_group(i):
    code = i.split()[1]
    if not code.isdigit() or len(code) != 5:  # продумать если возврат больше одной группы за раз
        return f'<ошибка в группе дат ({code})>'
    else:
        day = int(code[0]+code[1])
        month = code[2]+code[3]
        return f'<число: {day} месяц: {month}>'


def d_1_and_4_group(i):
    g = r.findall(r'[1|4]\d\d[\d/][\d/]', i)
    if not g:  # продумать если возврат больше одной группы за раз
        return ''
    else:
        g_dec = ''.join(g)
        h_snow = int(g_dec[1] + g_dec[2] + g_dec[3])
        if g_dec[0] == '1':
            return f'Высота снега (поле): {h_snow}, см'
        else:
            return f'Высота снега (лес): {h_snow}, см'


def d_2_and_5_group(i):
    g = r.findall(r'[2|5]\d\d[\d/][\d/]', i)
    if not g:  # продумать если возврат больше одной группы за раз
        return ''
    else:
        g_dec = ''.join(g)
        av_dens = int(g_dec[1] + g_dec[2]) / 100
        return f'Средняя плотность: {av_dens}, г/см3'


def d_3_and_6_group(d_1, d_2):
    h = r.findall(r'\d+', d_1)
    p = r.findall(r'\d+\.\d+', d_2)
    if h and p:
        d = float(p[0]) * 100
        H = round(int(h[0]) * d * 10 / 100)
        return f'Запас: {H}, мм'
    else:
        return ''


def encoder(data):
    result = ''
    for i in data:
        code = ' '.join(i.split()[2:])
        d_1 = d_1_and_4_group(code)
        d_2 = d_2_and_5_group(code)
        result += f'{decode_station(i)} {date_group(i)}' \
                  f'\n{d_1};  {d_2};  {d_3_and_6_group(d_1, d_2)}'
        if len(i.split()) > 5:
            code = ' '.join(i.split()[5:])
            d_4 = d_1_and_4_group(code)
            d_5 = d_2_and_5_group(code)
            result += f'\n{d_4};  {d_5};  {d_3_and_6_group(d_4, d_5)}'
        result += f'\n({i})\n\n'
    return result


def check_data(update: tg.Update, context: tg.ext.CallbackContext):
    data = [i for i in update.message.text.split('\n')]  # сгенерели словарь строк
    checked_code = [i[0:-1] for i in list(filter(lambda i: i.endswith('='), data))]
    # получили проверенные нужные данные, оканч-ся на =
    if not checked_code:
        message = '<нет удовлетворяющих условиям данных, подробнее в "справка">'
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        message = encoder(checked_code)
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)


check_data_handler = tg.ext.MessageHandler(tg.ext.Filters.text & (~tg.ext.Filters.command), check_data)
dispatcher.add_handler(check_data_handler)


start_handler = tg.ext.CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()