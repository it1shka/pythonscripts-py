import urllib.request
from bs4 import BeautifulSoup
req = urllib.request.Request(input('Введите адрес результатов\n'))
with urllib.request.urlopen(req) as response:
    page = response.read()
    soup = BeautifulSoup(page, 'html.parser')
    tables = soup.find_all('table')
    profile = input('Введите свой профиль так же, как на сайте\n')

    student_info = []
    
    for each in tables:
        parts = each.find_all('tr')
        for student in parts:
            fields = student.find_all('td')
            if len(fields) != 4:
                continue
            cur_info = {
                'number'    : fields[0].contents[0],
                'name'      : fields[1].contents[0],
                'profile'   : fields[2].contents[0],
                'mark'      : fields[3].contents[0]
            }
            if cur_info['profile'] == profile and cur_info['mark'] != 'не явился':
                student_info.append(cur_info)

    #сейчас у нас инфа по всем участникам в массиве student_info

    total = {}

    for each in student_info:
        name, mark = each['name'], int(each['mark'])
        if name in total:
            total[name] += mark
        else:
            total[name] = mark
    results = []

    for each in total:
        results.append((each, total[each]))

    results.sort(key=lambda x: x[1])
    results.reverse()

    name = input('Введите ваше ФИО, как на сайте\n')
    for each in results:
        if each[0] == name:
            print('{} {} {}'.format(each[0], each[1], '<======= YOU =======>'))
        else:
            print('{} {}'.format(each[0], each[1]))
