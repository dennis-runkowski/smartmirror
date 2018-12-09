from unittest import TestCase
from left_panel import YahooWeather


class TestYahooWeather(TestCase):
    def setUp(self):
        self.weather = YahooWeather("12760661")

    def test_get_current_weather(self):
        self.current_weather = self.weather.get_data()
        print self.current_weather
        self.assertTrue(self.current_weather)

        print self.weather.get_forecast[1:5]
        self.assertTrue(
            type(self.weather.get_forecast) is list)

        print self.weather.get_conditions
        self.assertTrue(
            type(self.weather.get_conditions) is dict)

