from models.gauges_1_1 import gauges_db
import re as r

def decode_name(i):  #проверяем наличие станции в базе данных
    code_st = i.split()[0]
    if code_st in gauges_db.keys():
        return f'{gauges_db[code_st]}'
    else:
        return '<нет такой станции>'

def date_group(i):
    g = i.split()[1]
    if not g.isdigit(): #продумать если возврат больше одной группы за раз
        return '<ошибка в группе дат>'
    else:
        day = int(g[0]+g[1])
        month = g[2]+g[3]
        return f'{day} {month}'

def d_1_group(i):
    g = r.findall(r'1\d{4}', i)
    if g == []:  # продумать если возврат больше одной группы за раз
        return ''
    else:
        g_dec = ''.join(g)
        h_snow = int(g_dec[1] + g_dec[2] + g_dec[3])
        return f'Высота снега (поле): {h_snow}, см'

def d_2_group(i):
    g = r.findall(r'2\d\d[\d/][\d/]', i)
    if g == []:  # продумать если возврат больше одной группы за раз
        return ''
    else:
        g_dec = ''.join(g)
        av_dens = int(g_dec[1] + g_dec[2]) / 100
        return f'Средняя плотность: {av_dens}, г/см3'

def d_3_group(d_1, d_2):
    for i in d_1.split():
        if not i.endswith(','):
            continue
        else:
            h = int(i[0:-1])
            for j in d_2.split():
                if not j.endswith(','):
                    continue
                else:
                    d = float(j[0:-1])
                    H = round(h * d * 10)
                    return f'Запас: {H}, мм'
                    break
                break
            break
        break

def d_4_group(i):
    g = r.findall(r'4\d\d[\d/][\d/]', i)
    if g == []:  # продумать если возврат больше одной группы за раз
        return ''
    else:
        g_dec = ''.join(g)
        h_snow = int(g_dec[1] + g_dec[2] + g_dec[3])
        return f'Высота снега (лес): {h_snow}, см'

def d_5_group(i):
    g = r.findall(r'5\d{4}', i)
    if g == []:  # продумать если возврат больше одной группы за раз
        return ''
    else:
        g_dec = ''.join(g)
        av_dens = int(g_dec[1] + g_dec[2]) / 100
        return f'Средняя плотность: {av_dens}, г/см3'

def d_6_group(d_4, d_5):
    for i in d_4.split():
        if not i.endswith(','):
            continue
        else:
            h = int(i[0:-1])
            for j in d_5.split():
                if not j.endswith(','):
                    continue
                else:
                    d = float(j[0:-1])
                    H = round(h * d * 10)
                    return f'Запас: {H}, мм'
                    break
                break
            break
        break


if __name__ == '__main__':
    with open('snow.txt', 'r') as f:
        with open('result.txt', 'w') as res:  # открыли входные данные
            f_read = f.read()  # прочитали
            users_code = [i for i in f_read.split('\n')]  # сгенерели словарь строк
            checked_code = [i[0:-1] for i in list(filter(lambda i: i.endswith('='), users_code))]
            # получили проверенные нужные данные, оканч-ся на =
            for i in checked_code:
                code = ' '.join(i.split()[2:])
                d_1 = d_1_group(code)
                d_2 = d_2_group(code)
                d_4 = d_4_group(code)
                d_5 = d_5_group(code)
                res.write(f'{decode_name(i)} {date_group(i)} {d_1}; {d_2}; {d_3_group(d_1, d_2)} {d_4}; {d_5}; {d_6_group(d_4, d_5)} ({i})' + '\n')