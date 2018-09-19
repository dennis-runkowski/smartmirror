"""This module contains all the plugins for the bottom banner."""
from datetime import datetime
import json
import os
import requests
import random
from bs4 import BeautifulSoup


class UsHolidays():
    def __init__(self, year, logger):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        base = root_dir.split('smartmirror')[0]
        file = 'smartmirror/smartmirror/data_files/{y}_holidays.json'.format(y=year)
        self.data_file = base + file
        self.year = year
        self.logger = logger

    def us_holidays(self):
        """Get all the us holidays."""
        today = datetime.now().strftime('%b %d %Y')

        if not os.path.exists(self.data_file):
            self.holiday_scraper()

        with open(self.data_file, 'r') as f:
            data = json.load(f)
            f.close()

        holidays = [i["Holiday"] for i in data if i["Dates"] == today]

        return holidays

    def holiday_scraper(self):
        """Scrape us holidays from https://www.timeanddate.com/holidays/us/year."""
        headers = {'Accept-Encoding': 'identity'}
        try:
            res = requests.get(
                'https://www.timeanddate.com/holidays/us/' + self.year,
                headers=headers
            )
        except Exception as e:
            self.logger.error(e)
            return

        raw_html = res.text
        if 'An error occurred' in raw_html:
            self.logger.error("Error scraping holiday data.")
            return

        html = BeautifulSoup(raw_html, 'html.parser')
        dates = []
        day = []
        for p in html.select('table'):
            for th in p.find_all("th", class_="nw"):
                dates.append(th.text)

            for a in p.select('a'):
                day.append(a.text)

        if len(dates) == len(day):
            holiday_dict = []
            for i in range(0, len(dates)):
                holiday_dict.append({
                    "Dates": dates[i] + ' ' + self.year,
                    "Holiday": day[i]
                })

        with open(self.data_file, 'w') as f:
            json.dump(holiday_dict, f)
            f.close()


class ChuckNorris():
    def __init__(self, logger):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        base = root_dir.split('smartmirror')[0]
        self.data_file = base + 'smartmirror/smartmirror/data_files/chuck_norris.json'
        self.logger = logger

    def joke(self):
        """Get a random chuck norris joke."""
        random_number = random.randint(0, 557)

        with open(self.data_file, 'r') as f:
            data = json.load(f)
            f.close()
        random_joke = data.get('value')[random_number]
        self.logger.debug("ChuckNorris random joke - %s", random_joke)

        return [random_joke["joke"]]
