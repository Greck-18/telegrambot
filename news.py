import requests
from bs4 import BeautifulSoup
import lxml


class News:
    def __init__(self, url):
        self.url = url
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, "lxml")
        self.news = []
        self.text = None
        self.title_text = None

    def get_info(self):
        list_news = self.soup.find_all("div",
                                       class_=("news-entry big annoticed time nip", "news-entry big annoticed time ni"))
        for item in range(len(list_news) // 3):
            self.news.append(
                {"title": list_news[item].find("span", class_="entry-head _title").get_text(strip=True).replace("\xa0",
                                                                                                                " "),
                 "text": list_news[item].find("span", class_="entry-note").get_text(strip=True).replace("\xa0", " "),
                 "time": list_news[item].find("span", class_="entry-time").get_text(strip=True).replace("\xa0", " "),
                 "url": list_news[item].find("a", class_="entry__link").get('href')})

    def news_page(self, count):
        while True:
            title = "<b>Заголовок:</b>" + "\n" + self.news[count - 1]['title'] + '\n'
            test = "<b>Текст:</b>\n" + self.news[count - 1]['text'] + '\n'
            time = "<b>Время публикации:</b> \n" + self.news[count - 1]['time'] + '\n'
            url = "<b>Ссылка:</b> \n" + self.news[count - 1]['url'] + '\n'
            self.text = title + test + time + url
            break
        return self.text

    def news_title(self):
        self.title_text = "Главные новости Беларуси на данный момент\n\n"
        for count, item in enumerate(self.news, start=1):
            self.title_text += str(count) + ':  ' + item['title'] + '\n' + '-' * 100 + '\n'
        return self.title_text



