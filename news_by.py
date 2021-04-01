# парсинг
import requests
from bs4 import BeautifulSoup
import lxml
import pprint as pp
from aiogram.utils.markdown import bold, italic, code, pre

URL = "https://news.tut.by/daynews/"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}


# запрос
def get_html(params=None):
    response = requests.get(URL, headers=HEADERS, params=params)
    return response


# получение инфы со страницы
def get_info_from_page(html):
    news = []
    soup = BeautifulSoup(html.text, "lxml")
    list_news = soup.find_all("div", class_=("news-entry big annoticed time nip", "news-entry big annoticed time ni"))
    for item in range(len(list_news) // 3):
        news.append(
            {"title": list_news[item].find("span", class_="entry-head _title").get_text(strip=True).replace("\xa0",
                                                                                                            " "),
             "text": list_news[item].find("span", class_="entry-note").get_text(strip=True).replace("\xa0", " "),
             "time": list_news[item].find("span", class_="entry-time").get_text(strip=True).replace("\xa0", " "),
             "url": list_news[item].find("a", class_="entry__link").get('href')})
    return news


# основная функция парсинга
def parse():
    html = get_html()
    nw = get_info_from_page(html)
    return nw


# функция отправки заголовков новостей
def title_of_news():
    news = parse()
    text = "Главные новости Беларуси на данный момент\n\n"
    for count, item in enumerate(news, start=1):
        text += str(count) + ':  ' + item['title'] + '\n' + '-' * 100 + '\n'
    return text


# функция отправка корректированного текста новостей
def page_of_news(count):
    text = None
    news = parse()
    while True:
        title = code("Заголовок:") + "\n" + news[count - 1]['title'] + '\n'
        test = "Текст:\n" + news[count - 1]['text'] + '\n'
        time = "Время публикации: \n" + news[count - 1]['time'] + '\n'
        url = "Ссылка: \n" + news[count - 1]['url'] + '\n'
        text = title + test + time + url
        break
    return text
