from pyowm import OWM
from pyowm.commons.exceptions import NotFoundError
from pyowm.utils import config
from pyowm.utils import timestamps

config = config.get_default_config()
config['language'] = 'ru'
API = "e1f39c775547e71adb46a1b632b9dd24"
owm = OWM(API, config)


# погода
class Weather:
    def __init__(self, city):
        self.city = city
        self.mgr = owm.weather_manager()
        try:
            self.observation = self.mgr.weather_at_place(self.city)
        except NotFoundError:
            self.city = "Бордо"
            self.observation = self.mgr.weather_at_place(self.city)
        self.w = self.observation.weather

    # self.forecast = self.mgr.forecast_at_place(self.city, 'daily')
    # self.answer = self.forecast.will_be_clear_at(timestamps.tomorrow())

    # получение погоды
    def get_weather(self):
        prompt = None
        if self.city == 'Бордо':
            return "Неизвестный город!"
        if self.w.temperature('celsius')['temp'] >= 21:
            prompt = "Уфффф,<strong> ну и жара на улице🥵</strong>, ты же сейчас в шортах и майке?)"
        elif 12 <= self.w.temperature('celsius')['temp'] <= 20:
            prompt = "<strong>Это не Майами</strong>,детка🙃, так что надевай штаны и jacket"
        else:
            prompt = "Бррррррр, холодрыга🥶, сейчас бы тёплого глинтвейна , а не вот это вот всё.<strong>Одевайся тепло!!!</strong>"

        return f"""Сечас в городе <strong>{self.city}</strong> {self.w.detailed_status}. Температура <strong>{int(self.w.temperature('celsius')['temp'])}℃</strong>
 и дует ветер со скоростью <strong>{self.w.wind()['speed']}м/c</strong>. """ + prompt
