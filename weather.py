from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config

config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM("e1f39c775547e71adb46a1b632b9dd24", config_dict)
mgr = owm.weather_manager()


class Weather:
    def __init__(self, city):
        self.city = city
        self.observation = mgr.weather_at_place(self.city)
        self.weather = self.observation.weather

    def get_weather(self):
        return f"Сейчас в городе {self.city}  температура {self.weather.temperature('celsius')['temp']}"



