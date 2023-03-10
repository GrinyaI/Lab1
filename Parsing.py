from bs4 import BeautifulSoup
import requests
import pandas

def parse(name):
    url=''
    try:
        url = 'https://omsk.hh.ru/search/vacancy?text='+str(name)+'&area=68'
    except:
        print('Подключение недоступно')

    headers = {
        'User-Agent': 'My User Agent 1.0',
        'From': 'youremail@domain.example'
    }
    page = requests.get(url, headers=headers)
    print(page.status_code)
    soup = BeautifulSoup(page.text, "html.parser")

    block = soup.findAll('div', class_='serp-item')

    serpitem = []
    vacimp = []
    vaccompen = []
    try:
        for data in block:
            work = data.find(class_='serp-item__title')
            boss = data.find(class_='bloko-link bloko-link_kind-tertiary')
            price = data.find('span', class_='bloko-header-section-3')
            if work is not None:
                serpitem.append(work.text)
            else:
                serpitem.append('-')

            if boss is not None:
                vacimp.append(boss.text.replace("\xa0"," "))
            else:
                vacimp.append('-')

            if price is not None:
                vaccompen.append(price.text.replace("\u202f",""))
            else:
                vaccompen.append('-')
    except:
        print('Не удалось выполнить запись в массивы')
    print(serpitem,vacimp, vaccompen)
    dat = {'Должность:':serpitem,'Работодатель:':vacimp,'Заработная плата:':vaccompen}
    pandas.DataFrame(dat).to_excel('Res.xlsx')