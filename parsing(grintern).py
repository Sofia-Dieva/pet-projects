import requests
from bs4 import BeautifulSoup
import json


url = 'https://www.grintern.ru/page/'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'ur user-agent'
}


blocks_info = {}
for num in range(1, 15):
    req = requests.get(url+str(num), headers)

    with open(f'data/{num}_prodjectp.html', 'w', encoding='utf-8') as file:
        file.write(req.text)

    with open(f'data/{num}_prodjectp.html', encoding='utf-8') as file:
        doc = file.read()

    soup = BeautifulSoup(doc, 'lxml')
    names = soup.find_all('div', class_='title')
    json_learning_dict = {}
    for i in names:
        if i.find('a') is not None:
            json_learning_dict[i.text.strip()] = 'https://www.grintern.ru'+i.find('a').get('href')

    with open(f'data/{num}_json_learning_dict.json', 'w', encoding='utf-8') as f:
        json.dump(json_learning_dict, f, indent=4, ensure_ascii=False)

    with open(f'data/{num}_json_learning_dict.json', encoding='utf-8') as file:
        vac = json.load(file)

    symb = [' ', '/', '"']

    for job, link in vac.items():
        for _ in symb:
            if _ in job:
                job = job.replace(_, '_')

        req = requests.get(url=link, headers=headers)
        src = req.text
        with open(f'data/{job}.html', 'w', encoding='utf-8') as f:
            f.write(src)
        with open(f'data/{job}.html', encoding='utf-8') as f:
            thing = f.read()

        soup = BeautifulSoup(thing, 'lxml')
        blocks = soup.find_all('h3')
        requirements = blocks[0].text
        conditions = blocks[1].text
        payment = blocks[2].text
        short_discription = 'Краткое описание'
        blocks_data = soup.find_all('div', class_='small')
        titels = [short_discription, requirements, conditions, payment]

        for item in range(len(blocks_data)):
            titels[item] = []
            if len(blocks_data[item].find_all('li')) != 0:
                for sent in blocks_data[item].find_all('li'):
                    titels[item].append(sent.text.lstrip('\n').capitalize())
            else:
                titels[item] = blocks_data[item].text.strip('\n')

        blocks_info[job] = {
                'Short description': titels[0],
                'Requirement': titels[1],
                'Conditions': titels[2],
                'Payment': titels[3]
            }


with open(f'data/jobs.json', 'w', encoding='utf-8') as file:
    json.dump(blocks_info, file, indent=4, ensure_ascii=False)
