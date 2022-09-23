#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Скрипт вывода криптопортфеля суммы и изменения его при старте системы
"""

import subprocess
import json;
import requests;
import datetime;
import time;
import os;

#Список крипты что есть, к доллару и сумма
crypts = {'DASHUSDT': 80.0485465,'ZECUSDT': 70.7856236,'XMRUSDT': 90.12112723};

#Обращаемся к api binance и выводим ошибку если нет сети
def get_price(price):
    try:
        r = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=' + price);
        resp = r.json()
        return float(resp['price']);
    except requests.ConnectionError:
        subprocess.call(["notify-send", "Нэт сэты !!!","-i","face-crying-symbolic.symbolic.png"])
        exit

#
def notify_display(icon, razzz):
    now = datetime.datetime.now()
    subprocess.call(["notify-send", message.format(now.strftime("(%d-%m-%Y) - (%H:%M:%S)"), all_text[:-1], all_sum, razzz),"-i", icon])


message = """
{}
= = = = = = = = = = = 
{}
= = = ALL = = =
Summ = {:.2f}
= = = = = = = = 
Cnange = {:.2f}
""" 

time.sleep(10)

#Вся крипта что есть
all_sum = 0
#Складываем состовляющие в текстовую переменную
all_text = ""


#Основной цикл программы
for x in crypts.items():
    #Вычесляем сумму по каждой криптовалюте
    all_sum += round(x[1] * get_price(x[0]), 2)
    #Формируем переменную которая выводит в тексте весь портфель
    all_text += x[0] + " " + str(round( x[1] * get_price(x[0]), 2) ) + "\n" 

#Читаем файл с суммой которая у была
with open('sum.txt', "r") as f:
    sum_file = f.readline()
    f.close()

#Записываем в файл новое значение 
with open('sum.txt', "w") as f:
    f.write(str(all_sum))
    f.close()


sum_file = float(sum_file)
all_sum = float(all_sum)

#В зависимости от + или - радоть ил груст
if sum_file > all_sum:
    notify_display("face-crying-symbolic.symbolic.png", all_sum - sum_file)
else:
    notify_display("face-angel-symbolic.symbolic.png", all_sum - sum_file)
