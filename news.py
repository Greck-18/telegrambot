import requests
from bs4 import BeautifulSoup
import lxml
from abc import ABC, abstractmethod
import pprint as pp
from beautifultable import BeautifulTable


class NewsParser(ABC):
    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def process_data(self):
        pass

    @abstractmethod
    def get_news(self):
        pass


class NewsBy(NewsParser):
    _url = "https://news.tut.by/daynews/"
    _headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}

    def __init__(self):
        self.news = []
        self.text = None
        self.title_text = None

    def get_data(self):
        response = requests.get(self._url, self._headers)
        if response.ok:
            self.soup = BeautifulSoup(response.text, "lxml")
        else:
            raise ValueError(f"Error: {response.status_code}")

    # получение html и упорядочивание
    def process_data(self):
        try:
            content = self.soup.find_all("div",
                                         class_=(
                                             "news-entry big annoticed time nip", "news-entry big annoticed time ni"))
            for item in range(len(content) // 3):
                self.news.append(
                    {"title": content[item].find("span", class_="entry-head _title").get_text(strip=True).replace(
                        "\xa0",
                        " "),
                        "text": content[item].find("span", class_="entry-note").get_text(strip=True).replace("\xa0",
                                                                                                             " "),
                        "time": content[item].find("span", class_="entry-time").get_text(strip=True).replace("\xa0",
                                                                                                             " "),
                        "url": content[item].find("a", class_="entry__link").get('href')})
        except AttributeError:
            raise AttributeError("Call method get_data()")

    # основной текст новостей с ссылкой на расширенную версию новостей
    def get_news(self, count):
        while True:
            title = "<b>Заголовок:</b>" + "\n" + self.news[count - 1]['title'] + '\n'
            test = "<b>Текст:</b>\n" + self.news[count - 1]['text'] + '\n'
            time = "<b>Время публикации:</b> \n" + self.news[count - 1]['time'] + '\n'
            url = "<b>Ссылка:</b> \n" + self.news[count - 1]['url'] + '\n'
            self.text = title + test + time + url
            break
        return self.text

    # заголовки новостей
    def get_title(self):
        self.title_text = "Главные новости Беларуси на данный момент\n\n"
        for count, item in enumerate(self.news, start=1):
            self.title_text += str(count) + ':  ' + item['title'] + '\n' + '-' * 100 + '\n'
        return self.title_text


class FootBallNews(NewsParser):
    _url = "https://ru.uefa.com/memberassociations/leaguesandcups/"
    _headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}

    def __init__(self):
        self.table = BeautifulTable()
        self.team = []
        self.game = []
        self.point = []

    def get_data(self):
        response = requests.get(self._url, self._headers)
        if response.ok:
            self.soup = BeautifulSoup(response.text, "lxml")
        else:
            raise ValueError(f"Error: {response.status_code}")

    def process_data(self):
        try:
            team = self.soup.find_all("span", class_="table_team-name_block")
            game = self.soup.find_all("td", class_="table_team-played js-played")  # .get_text(strip=True)
            point = self.soup.find_all("td", class_="table_team-points js-points")
            # .get_text(strip=True)

            for i in range(len(team)):
                lis = [team[i]['title'] for j in range(5)]
                self.team.append(lis)
                lis1 = [game[j].get_text() for j in range(5)]
                self.game.append(lis1)
                lis2 = [point[i].get_text() for j in range(5)]
                self.point.append(lis2)

        except AttributeError:
            raise AttributeError("Call method get_data()")

    def get_news(self, count):
        self.table.set_style(BeautifulTable.STYLE_RST)
        self.table.columns.header = ['team', 'game', 'point']
        self.table.rows.header = ['1', '2', '3', '4', '5']
        for i in range(5):
            self.table.rows[i] = [self.team[i][count], self.game[i][count], self.point[i][count]]

        print(self.table)
        print(self.team)
        print(self.game)



foot = FootBallNews()
foot.get_data()
foot.process_data()
foot.get_news(3)
