from models.gauges_1_1 import gauges_db
import re

f = open('snow.txt', 'r') #открыли входные данные
users_code = f.read().split('\n') #получили словарь из строк их входных данных

checked_code = '' #получили проверенные нужные данные, оканч-ся на =
for i in users_code:
    if i.endswith('='):
        i = i[0:-1]
        checked_code += i + '\n'

#print(checked_code)

name_g = ''


clear_code = checked_code.split('\n')
#print(clear_code)

def ind(i, i_s):
    del i_s[0:2]
    for i in i_s:
        if list(i)[0] == 1:
#        print(list(i)[0])
            h_snow = list(i)[1]+list(i)[2]+list(i)[3]
            return f'Высота снега: {h_snow}'


for i in clear_code:
    i_s = i.split(' ')
#    print(i_s)
    for i in i_s:
        if i in gauges_db.keys():
            try:
                lst = list(i_s[1])
                day = int(lst[0]+lst[1])
                month = lst[2]+lst[3]
                print(i_s)
                ind(i, i_s)
                print(i_s)
                name_g += f'{i} {decode(i)} {day}.{month} {ind(i, i_s)}'+'\n'
            except IndexError:
                name_g += f'{i} {decode(i)}'+'\n'


#    lst = list[i]
#    if lst[0] == 1
    
    


print(name_g)

f.close()




#    else:
#        print(f'<нет такой станции {i}>')


