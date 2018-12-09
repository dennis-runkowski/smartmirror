"""This Module contains all the plugins from the left panel."""

import requests
import json
import time


class WunderGround():
    """Weather: current and forecast from wunderGround."""

    def __init__(self, api_key, state, zipcode, logger):
        """Construct the keys to use this class."""
        # self.logger = logger
        self.api_key = api_key
        self.state = state
        self.area = zipcode
        self.conditions = {
            'Rain': '/static/img/icons/Rain.png',
            'Overcast': '/static/img/icons/Cloud.png',
            'Drizzle': '/static/img/icons/Rain.png',
            'Snow': '/static/img/icons/Snow.png',
            'Ice': '/static/img/icons/Snow.png',
            'Mist': '/static/img/icons/Rain.png',
            'Fog': '/static/img/icons/Haze.png',
            'Cloud': '/static/img/icons/Cloud.png',
            'Cloudy': '/static/img/icons/Cloud.png',
            'Clear': '/static/img/icons/Sun.png',
            'Sunny': '/static/img/icons/Sun.png',
            'Funnel': '/static/img/icons/Tornado.png',
            'Hail': '/static/img/icons/Hail.png',
            'Squalls': '/static/img/icons/Wind.png',
            'Spray': '/static/img/icons/Rain.png',
            'Partly': '/static/img/icons/PartlySunny.png',
            'Thunderstorms': '/img/static/icons/Storm.png',
            'Thunderstorm': '/img/static/icons/Storm.png',
            'Unknown': '/static/img/icons/Sun.png'
        }
        self.logger = logger

    def current(self):
        """Current Weather Data from Wunderground."""
        try:
            data = requests.get(
                'http://api.wunderground.com/api/'
                '{key}/geolookup/conditions/q/{s}/{z}.json'
                .format(key=self.api_key, s=self.state, z=self.area))

            weather_data = json.loads(data.content)
            current_observation = weather_data["current_observation"]
            cur_wx = {}

            cur_wx["weather"] = current_observation["weather"]
            cur_wx["temp"] = current_observation["temperature_string"]
            cur_wx["temp_f"] = current_observation["temp_f"]
            cur_wx["humidity"] = current_observation["relative_humidity"]
            cur_wx["date"] = current_observation["local_time_rfc822"]
            cur_wx["icon"] = current_observation["icon_url"]
            cur_wx["city"] = weather_data["location"]["city"]
            cur_wx['link'] = ""

            for wx, icon in self.conditions.iteritems():
                if wx in cur_wx['weather']:
                    cur_wx['link'] = icon
                    break

        except requests.exceptions.RequestException as e:
            self.logger.error("Current Weather: {error}".format(error=e))
            cur_wx = {
                "weather": "Null",
                "temp": "Null",
                "temp_f": "Null",
                "humidity": "Null",
                "date": "Null",
                "icon": "Null",
                "city": "Null",
                "link": "/static/img/icons/error.png"
            }

        except ValueError as e:
            self.logger.error("Current Weather: {error}".format(error=e))
            cur_wx = {
                "weather": "Null",
                "temp": "Null",
                "temp_f": "Null",
                "humidity": "Null",
                "date": "Null",
                "icon": "Null",
                "city": "Null",
                "link": "/static/img/icons/error.png"
            }

        return cur_wx

    def forecast(self):
        """Hourly forecast from Wunderground."""
        try:
            data = requests.get(
                "http://api.wunderground.com/api/"
                "{key}/hourly/q/{s}/{z}.json"
                .format(key=self.api_key, s=self.state, z=self.area))

            hourly_data = json.loads(data.content)

            hourly = []

            for weather in hourly_data["hourly_forecast"]:

                temp = {}
                temp["time"] = weather["FCTTIME"]["civil"]
                temp["temp"] = weather["temp"]["english"]
                temp["condition"] = weather["condition"]

                for wx, icon in self.conditions.iteritems():
                    if wx in weather["condition"]:
                        temp['link'] = icon
                        break
                hourly.append(temp)

        except requests.exceptions.RequestException as e:
            self.logger.error("Forecast: {error}".format(error=e))
            hourly = [{
                "time": "Error",
                "temp": "Loading",
                "condition": "Data"
            }]

        except ValueError as e:
            self.logger.error("Forecast: {error}".format(error=e))
            hourly = [{
                "time": "Error",
                "temp": "Loading",
                "condition": "Data"
            }]

        return hourly

    def current_with_forecast(self):
        """Return json with current weather and the hourly forecast."""
        current = self.current()
        forecast = self.forecast()

        data = {
            "current": current,
            "forecast": forecast[:4]
        }

        return data


class StockData(object):
    """Stock data from Alpha Advantage."""

    def __init__(self, api_key, tickers, logger):
        """Setup required parameters."""
        self.api_key = api_key
        self.tickers = tickers
        self.logger = logger

    def get_stock_price(self):
        """Get the current stock price."""
        data = {}
        for ticker in self.tickers:
            try:
                res = requests.get(
                    "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&"
                    "symbol={s}&apikey={key}".format(s=ticker, key=self.api_key)
                )
                res_json = json.loads(res.text)
                data[ticker] = res_json.get("Global Quote").get("05. price")
            except Exception as e:
                self.logger.error(e)
                data[ticker] = 'N/A'

            # respect the alpha advantage rate limit
            time.sleep(1)
        return data


class YahooWeather(object):
    """
    Yahoo Weather api

    The location identifier can be found by looking up your city/state
    on yahoo.com and extracting the woeid from the url.

    Attributes:
        woeid (str): Unique location identifier
    """
    def __init__(self, woeid):
        """Inits YahooWeather with woeid and base_url."""
        self.woeid = woeid
        # Base url for the public yahoo api
        self.base_url = "https://query.yahooapis.com/v1/public/yql?"
        # Weather data
        self.data = {}
        # Dict containing all the icons
        self.conditions = {
            "tropical storm": "/static/img/icons/Storm.png",
            "hurricane": "/static/img/icons/Storm.png",
            "tornado": "/static/img/icons/Tornado.png",
            "severe thunderstorms": "/static/img/icons/Storm.png",
            "thunderstorms": "/static/img/icons/Storm.png",
            "mixed rain and snow": "/static/img/icons/Snow.png",
            "rain and snow": "/static/img/icons/Snow.png",
            "mixed rain and sleet": "/static/img/icons/Rain.png",
            "rain": "/static/img/icons/Rain.png",
            "mixed snow and sleet": "/static/img/icons/Snow.png",
            "freezing drizzle": "/static/img/icons/Snow.png",
            "drizzle": "/static/img/icons/Rain.png",
            "freezing rain": "/static/img/icons/Rain.png",
            "showers": "/static/img/icons/Rain.png",
            "snow flurries": "/static/img/icons/Snow.png",
            "light snow showers": "/static/img/icons/Snow.png",
            "blowing snow": "/static/img/icons/Snow.png",
            "snow": "/static/img/icons/Snow.png",
            "hail": "/static/img/icons/Hail.png",
            "sleet": "/static/img/icons/Hail.png",
            "dust": "/static/img/icons/Haze.png",
            "foggy": "/static/img/icons/Haze.png",
            "haze": "/static/img/icons/Haze.png",
            "smoky": "/static/img/icons/Haze.png",
            "blustery": "/static/img/icons/Wind.png",
            "windy": "/static/img/icons/Wind.png",
            "cold": "/static/img/icons/Sun.png",
            "cloudy": "/static/img/icons/Cloud.png",
            "mostly cloudy (night)": "/static/img/icons/PartlyMoon.png",
            "mostly cloudy (day)": "/static/img/icons/PartlySunny.png",
            "mostly sunny": "/static/img/icons/PartlySunny.png",
            "mostly cloudy": "/static/img/icons/Cloud.png",            "partly cloudy (night)": "/static/img/icons/PartlyMoon.png",
            "partly cloudy (day)": "/static/img/icons/PartlySunny.png",
            "clear (night)": "/static/img/icons/Moon.png",
            "sunny": "/static/img/icons/Sun.png",
            "fair (night)": "/static/img/icons/Moon.png",
            "fair (day)": "/static/img/icons/Sun.png",
            "mixed rain and hail": "/static/img/icons/Hail.png",
            "hot": "/static/img/icons/Sun.png",
            "isolated thunderstorms": "/static/img/icons/Storm.png",
            "scattered thunderstorms": "/static/img/icons/Storm.png",
            "scattered showers": "/static/img/icons/Rain.png",
            "heavy snow": "/static/img/icons/Snow.png",
            "scattered snow showers": "/static/img/icons/Snow.png",
            "partly cloudy": "/static/img/icons/Cloud.png",
            "thundershowers": "/static/img/icons/Storm.png",
            "snow showers": "/static/img/icons/Snow.png",
            "isolated thundershowers": "/static/img/icons/Storm.png",
            "not available": "/static/img/icons/Sun.png"
        }

    def get_data(self):
        """
        Get the weather data for a location.

        Returns:
            A json containing the current weather.
        """
        yql_query = u"select * from weather.forecast where woeid={_id}".format(
            _id=self.woeid
        )
        parameters = {
            "q": yql_query,
            "format": "json"
        }
        try:
            data = requests.get(self.base_url, params=parameters)
        except Exception as a:
            raise e

        data_check = data.json().get("query", None)
        if data_check:
            res = data_check["results"]["channel"]
            self.data = res
            return True

        return False

    @property
    def get_forecast(self):
        """:obj: `list` get the weather forecast
        """
        forecast = self.data.get("item", {}).get("forecast", [])
        for idx, conditions in enumerate(forecast):
            temp_text = conditions.get("text", "not available")
            icon_path = self.get_link(temp_text)
            forecast[idx]["link"] = icon_path
        return forecast

    @property
    def get_conditions(self):
        """:obj: `dict` get the current weather
        """
        conditions = self.data.get("item", {}).get("condition", {})
        city = self.data.get("location", {}).get("city", "")
        text = conditions.get("text")
        icon_link = self.get_link(text)
        conditions["link"] = icon_link
        conditions["location"] = city
        return conditions

    def get_link(self, text):
        """
        Method to get the right icon link from the condition text.

        Args:
            text (str): Text for the current weather condition
        Returns:
            String containing the path to the icon.
        """

        normalize_text = text.lower()
        return self.conditions.get(normalize_text, "/static/img/icons/Sun.png")