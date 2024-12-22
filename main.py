from bs4 import BeautifulSoup
import requests
import sqlite3

temperatura = []
date_day = []

responce = requests.get('https://sinoptik.ua/')

if responce.status_code == 200:

    item_site = BeautifulSoup(responce.text, features='html.parser')
    date = item_site.findAll('p', {'class', 'BzO81ZRx'})
    temperature = item_site.findAll('div', {'class', 'XyT+Rm+n'})

    for information2 in temperature:
        temperatura_vetra = information2.findNext().text[4:]
        temperatura.append(temperatura_vetra)

    for information in date:
        day = information.findNext().text[0:]
        date_day.append(day)

# print('Число ->', date_day)
# print('Температура ветра ->', temperatura)

connection = sqlite3.connect('allInformation_db.sl3')
cur_db = connection.cursor()

# cur_db.execute("CREATE TABLE date_day (date_day, temperatura TEXT);")


for i in range(len(temperatura)):
    # print(temperatura[i])
    cur_db.execute("INSERT INTO date_day (temperatura) VALUES (?)", (temperatura[i],))

for i in range(len(date_day)):
    # print(date_day[i])
    cur_db.execute("INSERT INTO date_day (date_day) VALUES (?)", (date_day[i],))

# Понятия не имею, почему там написано None, но вторая "строчка" это дата (там где написано 22, 23, 24 и т.д.)
cur_db.execute("SELECT date_day, temperatura FROM date_day;")
DateWeather = cur_db.fetchall()
print('Results from DB ->', DateWeather)

connection.commit()
connection.close()