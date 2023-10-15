from bs4 import BeautifulSoup
import requests
from os import system, startfile, name
from colorama import init, Fore, Back, Style
import random
import re
from time import sleep

# colorama
init(autoreset=False)


def print_col(col, text, func_col=None, platform_col=None, end=False):
    colors = {
        'ж': Fore.YELLOW,
        'к': Fore.LIGHTRED_EX,
        'з': Fore.GREEN,
        'ск': Fore.RED + Style.BRIGHT,
        'с': Fore.LIGHTBLACK_EX,
        'г': Fore.CYAN,
        'ф': Fore.LIGHTMAGENTA_EX,
        'б': Fore.BLUE
    }
    priset = colors.get(col.lower(), Fore.LIGHTBLACK_EX)

    if func_col is None:
        if end:
            print(priset + text, end='')
        else:
            print(priset + text, end='')
            print(Style.RESET_ALL + Back.RESET + Fore.RESET)
    else:
        if platform_col == 'win':
            print(priset, end='')
            x = func_col(text)
            print(Style.RESET_ALL + Back.RESET + Fore.RESET, end='')
            return x
        x = func_col(priset + text)
        print(Style.RESET_ALL + Back.RESET + Fore.RESET, end='')
        return x


def Loading_data() -> dict:
    while True:
        print_col("с", " Загрузка данных c wikipedia . . .")
        try:
            url = "https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%81%D1%82%D0%BE%D0%BB%D0%B8%D1%86_%D0%B3%D0%BE%D1%81%D1%83%D0%B4%D0%B0%D1%80%D1%81%D1%82%D0%B2"
            page = requests.get(url, timeout=3)
            soup = BeautifulSoup(page.text, "lxml")
            table = soup.find_all("table", class_="wikitable")
            # print(table)
            countries_capitals = {}
            for i in table:
                rows = i.find_all("tr")[1:]
                for row in rows:
                    cells = row.find_all("td")
                    country = re.sub(r'\[.*\]', '', cells[1].text.strip().capitalize())
                    capital = re.sub(r'\[.*\]', '', cells[2].text.strip().capitalize())
                    if cells[2]('a'):
                        link = cells[2].find('a').get('href')
                    else:
                        link = None
                    countries_capitals[country] = capital, link
            # print(countries_capitals)
            # with open('capitals.json', 'w') as f:
            #     json.dump(countries_capitals, f, ensure_ascii=False, indent=2)
            sleep(2)
            system('cls')
            return countries_capitals
        except Exception:
            print_col("к", 'Произошла непредвиденная ошибка возможно интернет-соединение недоступно.')
            print_col("c", 'Попробовать снова - "Enter"', input, 'win')
            system('cls')


def open_wiki(link):
    """открыть страницу в wikipedia"""
    if not link is None:

        wiki_url = f'https://ru.wikipedia.org{link}'

        if name == 'nt':  # для Windows
            startfile(wiki_url)
        elif name == 'posix':  # для macOS и Linux
            system(f'open "{wiki_url}"')

    else:
        print_col("ж", "Извините к сожалению ссылка на ресурс отсутствует ( мда")


def calculate_grade(student_bal):
    """Определяет оценку студента по пятибалльной шкале на основе списка результатов"""
    correct_answers = sum(student_bal)  # сумма правильных ответов
    total_questions = len(student_bal)  # общее количество вопросов
    percentage = correct_answers / total_questions * 100  # процент правильных ответов
    if percentage >= 90:
        return ("5 :) отлично!!!", percentage)
    elif percentage >= 75:
        return ("4 :) хорошо!", percentage)
    elif percentage >= 50:
        return ("3 :( мда", percentage)
    elif percentage >= 25:
        return ("2 :( труба", percentage)
    return ("1 :( капец", percentage)


def testing_print(n: int, d: dict) -> [None, str]:
    result = []
    count = 0
    right_answers = {}
    kp = 80
    for _ in range(n):
        count += 1
        question = random.choice(tuple(d.keys()))

        response = {d[question]}
        while len(response) != 4:
            response.add(random.choice(tuple(d.values())))
        voreants = ['А', 'Б', 'В', 'Г']
        random.shuffle(voreants)
        response = {k: v for k, v in zip(voreants, response)}

        system('cls')
        print_col("с", '-' * kp)
        print_col("г", f" Вопрос № {count}")
        print_col("с", '-' * kp)
        print_col("г", f' Какой город является столицей страны "{question}" ?:')
        print_col("г", f" А) {response['А'][0]}")
        print_col("г", f" Б) {response['Б'][0]}")
        print_col("г", f" В) {response['В'][0]}")
        print_col("г", f" Г) {response['Г'][0]}")
        print_col("с", '-' * kp)

        right_answers[count] = ''.join(k for k, v in response.items() if d[question] == v)

        while True:
            usr_otvet = print_col("ж", ' Ваш ответ (а,б,в,г) нажать "Enter": ', input, 'win').upper()
            if usr_otvet in voreants:
                break

        if d[question] == response[usr_otvet]:
            result.append(True)
            print_col("з", ' ВЕРНО!!!')
        else:
            result.append(False)
            print_col("ск", f' НЕВЕРНО "{d[question][0]}" вариант "{right_answers[count]}"')

        if print_col("с",
                    ' Хочешь узнать больше о столице и открыть для себя новое\n введи цифру 1, продолжить "Enter": ',
                    input, 'win') == '1':
            open_wiki(d[question][1])
            sleep(3)

    system('cls')
    print_col("с", '-' * kp)
    print_col("г", " Результат тестирования")
    print_col("с", '-' * kp)
    grade, percent = calculate_grade(result)
    print_col("ж", f" Доля правильных ответов составила - {int(percent)}%")
    print_col("ск", f" Ваша оценка - {grade}")
    # print_col("с", f' Ответы к вариантам: ', end=True)
    # print(*right_answers.items())
    print_col("с", '-' * kp)


def main():
    system("title Checking capitals (author Eugene Build 102)  ^<МАСШТАБИРОВАНИЕ CTRL + КОЛ.МЫШИ^>")
    flag = True
    number_test = 10
    countries_capitals = Loading_data()
    while True:
        if flag:
            print_col("г", " Эта программа поможет тебе проверить знание столиц разных стран. При тестировании")
            print_col("г",
                    f" ты познакомишься со столицами {len(countries_capitals.keys())} стран! Готов начать проверку своих знаний географии?")
            print_col("г",
                    f" Подготовься к {number_test} вопросам и докажи, что ты знаешь, где находятся столицы всех этих стран.")
            print_col("с", ' Начать (нажать "Enter")', input, 'win')
            system('cls')
            flag = False

        testing_print(number_test, countries_capitals)
        print_col("с", ' Пройти тест снова (нажать "Enter")', input, 'win')
        system('cls')


if __name__ == '__main__':
    main()
