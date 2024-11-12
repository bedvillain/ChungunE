import requests
from bs4 import BeautifulSoup

def get_school_meals():
    url = "https://school.use.go.kr/hcu-h/M01080101/list"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    breakfast_menu = []
    lunch_menu = []
    dinner_menu = []

    # 각 급식 정보를 담고 있는 'li' 태그 추출
    meal_sections = soup.find_all('li', class_='tch-lnc-wrap')

    if len(meal_sections) >= 3:
        # 조식 메뉴 크롤링
        breakfast_items = meal_sections[0].find_all('li')
        for item in breakfast_items:
            breakfast_menu.append(item.text.strip())

        # 중식 메뉴 크롤링
        lunch_items = meal_sections[1].find_all('li')
        for item in lunch_items:
            lunch_menu.append(item.text.strip())

        # 석식 메뉴 크롤링
        dinner_items = meal_sections[2].find_all('li')
        for item in dinner_items:
            dinner_menu.append(item.text.strip())

    return breakfast_menu, lunch_menu, dinner_menu
