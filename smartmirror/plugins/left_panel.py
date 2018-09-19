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
            'Clear': '/static/img/icons/Sun.png',
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
