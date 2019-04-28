"""This Module contains all the plugins from the left panel."""

import requests
import json
import time
from datetime import datetime, timedelta


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
            "mostly cloudy (day)": "/static/img/icons/Cloud.png",
            "mostly sunny": "/static/img/icons/Sun.png",
            "mostly cloudy": "/static/img/icons/Cloud.png",
            "partly cloudy (night)": "/static/img/icons/PartlyMoon.png",
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
            "partly cloudy": "/static/img/icons/PartlySunny.png",
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
        except Exception as e:
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

class OpenWeather(object):
    """
    Open Weather api

    https://openweathermap.org/api

    This method uses the lon/lat to find the weather for your city.
    You can look up the coordinates on https://openweather.org

    Attributes:
        lon (str): Longitude
        lat (str): Latitude
        api_key (str): OpenWeather api key
        logger (obj): logging handle
    """

    def __init__(self, lon, lat, api_key, logger):
        """Inits OpenWeather with lon and lat."""
        self.lon = lon
        self.lat = lat
        self.api_key = api_key
        self.logger = logger
        self.base_url = "https://api.openweathermap.org/data/2.5/"
        self.icons = {
            "01d": "/static/img/icons/Sun.png",
            "01n": "/static/img/icons/Moon.png",
            "02d": "/static/img/icons/PartlySunny.png",
            "02n": "/static/img/icons/PartlyMoon.png",
            "03d": "/static/img/icons/Cloud.png",
            "03n": "/static/img/icons/Cloud.png",
            "04d": "/static/img/icons/PartlySunny.png",
            "04n": "/static/img/icons/PartlyMoon.png",
            "09d": "/static/img/icons/Rain.png",
            "09n": "/static/img/icons/Rain.png",
            "10d": "/static/img/icons/Rain.png",
            "10n": "/static/img/icons/Rain.png",
            "11d": "/static/img/icons/Storm.png",
            "11n": "/static/img/icons/Storm.png",
            "13d": "/static/img/icons/Snow.png",
            "13n": "/static/img/icons/Snow.png",
            "50d": "/static/img/icons/Haze.png",
            "50n": "/static/img/icons/Haze.png"
        }

    def current_weather(self, units="imperial"):
        """
        Get the current weather for a location. Units default to imperial for
        the USA.

        Parameters:
            units (str): units F=imperial, C=metric , K=standard

        Returns:
            data (obj): dict containing the current weather
        """
        if units != "imperial":
            if units == "metric":
                self.logger.info("Using metric.")
            elif units == "standard":
                self.logger.info("Using kelvin.")
            else:
                self.logger.error("Unknown unit type defaulting to imperial.")
                units = "imperial"


        url = "{b}weather?lat={lat}&lon={lon}&units={units}&appid={api}".format(
            b=self.base_url,
            lat=self.lat,
            lon=self.lon,
            units=units,
            api=self.api_key
        )
        try:
            res = requests.get(url)
        except Exception as e:
            self.logger.error(e)
            return {}

        data = res.json()
        icon = data.get("weather", [""])[0].get("icon", "")


        weather = {
            "temp": int(round(data.get("main", {}).get("temp", ""))),
            "location": data.get("name", ""),
            "icon": self.icons.get(icon,),
            "description": data.get("weather", [""])[0].get("description", ""),
            "units": units
        }
        return weather

    def forecast(self, forecast_type="daily", units="imperial"):
        """
        OpenWeather forecast for the next 7 days or hourly.

        Parameters:
            forecast_type (str): hourly or daily weather forecast
            units (str): units F=imperial, C=metric , K=standard

        Returns:
             forecast (obj): list containing the weather forecast
        """
        if units != "imperial":
            if units == "metric":
                self.logger.info("Using metric.")
            elif units == "standard":
                self.logger.info("Using kelvin.")
            else:
                self.logger.warn("Unknown unit type defaulting to imperial.")
                units = "imperial"

        if forecast_type != "daily":
            if forecast_type == "hourly":
                self.logger.info("Getting hourly forecast")
            else:
                self.logger.warn("Unknown type, using daily default")
                forecast_type = "daily"

        url = "{b}forecast?lat={lat}&lon={lon}&units={u}&appid={api}".format(
            b=self.base_url,
            lat=self.lat,
            lon=self.lon,
            u=units,
            api=self.api_key
        )
        try:
            res = requests.get(url)
        except Exception as e:
            self.logger.error(e)
            return {}

        data = res.json()
        forecast_hourly = []
        for i in data.get("list", []):
            temp_icon = i.get("weather", [""])[0].get("icon", "")
            # Convert datetime
            try:
                date_obj = datetime.strptime(
                    i.get("dt_txt"), '%Y-%m-%d %H:%M:%S')
                new_date = date_obj.strftime("%Y-%m-%d %I:%M:%S %p")
            except:
                new_date = i.get("dt_txt")
            temp = {
                "temp_min": int(round(i.get("main", {}).get("temp_min", ""))),
                "temp_max": int(round(i.get("main", {}).get("temp_max", ""))),
                "temp": int(round(i.get("main", {}).get("temp", ""))),
                "description": i.get("weather", [""])[0].get("description", ""),
                "icon": self.icons.get(temp_icon, ""),
                "date": new_date
            }
            forecast_hourly.append(temp)

        if forecast_type == "hourly":
            return forecast_hourly

        forecast_daily = []
        forecast_dates = [datetime.now() + timedelta(days=i) for i in
                          range(1, 6)]
        for i in forecast_dates:
            temp_dt_string = datetime.strftime(i, "%Y-%m-%d")
            temp_list = []
            description_count = {}
            for f in forecast_hourly:
                if temp_dt_string in f["date"]:
                    temp_list.append(f["temp"])
                    if description_count.get(f["description"]):
                        description_count[f["description"]] += 1
                    else:
                        description_count[f["description"]] = 1
            if not description_count:
                break

            condition = max(description_count,
                            key=lambda key: description_count[key])
            icon = ''
            for f in forecast_hourly:
                if f.get("description") == condition:
                    icon = f.get("icon")
                    break
            temp_daily = {
                "date": temp_dt_string,
                "description": condition,
                "temp_high": max(temp_list),
                "temp_low": min(temp_list),
                "temp": int(round((sum(temp_list)/len(temp_list)))),
                "icon": icon
            }
            forecast_daily.append(temp_daily)

        return forecast_daily

