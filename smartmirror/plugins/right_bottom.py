"""These classes contain all the plugins for the right bottom banner."""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, time
import feedparser
import random
from ..models.models import NJTModel, APIlimit


class NJTPlugin():
    def __init__(self, logger):
        """Setting up logger."""
        self.logger = logger

    def update_njt_schedule(self, password, username, station, direction):
        """Update NJT schedule in main.db."""
        last_time_stamp = NJTModel.get_last_update()
        incr_date = date.today()

        # Dont run between 12am and 1210am
        current_time = datetime.now().time()
        if current_time <= time(00, 30):
            self.logger.warn("Exit early cool off period")
            return

        if not last_time_stamp:
            self.logger.info("First run, load db")
        elif incr_date <= last_time_stamp:
            self.logger.info("Database is up to date!")
            return

        try:
            count = APIlimit.get_row('njt')
            if count:
                update_count = APIlimit('njt', count.request_count)
                # check reset
                if count.request_count > 5:
                    update_count.reset_counter()
                    self.logger.warn("Backing off njt schedule request")
                    return
                else:
                    self.logger.warn("Updating api counter.")
                    update_count.update_counter()
            else:
                set_count = APIlimit('njt', 1)
                set_count.save_to_db()

            data = requests.get(
                'http://traindata.njtransit.com:8092/'
                'njttraindata.asmx/getStationScheduleXML'
                '?username={un}&password={pword}&station={st}&NJT_Only={nj}'
                .format(un=username, pword=password, st=station, nj='yes'))

            soup = BeautifulSoup(data.text, "html5lib")

        except requests.exceptions.RequestException as e:
            self.logger.error(e)
            raise e

        schedule_data = []
        for schedule in soup.find_all('item'):
            if schedule.direction.text == direction:
                schedule_data.append(schedule.sched_dep_date.text)

        if len(schedule_data) == 0:
            self.logger.warn("No data was pulled!")
            return

        try:
            NJTModel.delete_all()
            self.logger.warn("Updating NJT schedule")
            self.logger.warn(schedule_data)
            for row in schedule_data:
                _row = NJTModel(row, direction, incr_date)
                _row.save_to_db()

        except Exception as e:
            self.logger.error(e)
            raise e

    def get_njt_schedule(self):
        """Get njt schedule from main.db."""
        return NJTModel.query_all()

    def njt_departure(self, password, username, station):
        """Get NJT departure Vision."""
        train_status = []
        bad_request = {
            'station': 'Null',
            'status': 'Null',
            'sec_late': 'Null'
        }

        # Stop api if it is between 1100pm and 5am
        current_time = datetime.now().time()
        if current_time >= time(23, 00):
            bad_request["status"] = "goodnight"
            train_status.append(bad_request)

            return train_status

        elif current_time <= time(05, 00):
            bad_request["status"] = "goodnight"
            train_status.append(bad_request)

            return train_status

        try:
            data = requests.get(
                'http://traindata.njtransit.com:8092/'
                'njttraindata.asmx/getTrainScheduleXML'
                '?username={un}&password={pword}&station={st}'
                .format(un=username, pword=password, st=station))

            soup = BeautifulSoup(data.text, "html5lib")

        except Exception as e:
            self.logger.error(e)
            train_status.append(bad_request)

            return train_status

        count = 0
        for item in soup.find_all('item'):

            count += 1
            temp_dict = {}

            if item.status.text == ' ':
                status = 'TBD'
            else:
                status = item.status.text

            temp_dict['station'] = str(item.destination.text)
            temp_dict['status'] = str(status)
            temp_dict['sec_late'] = str(item.sec_late.text)

            train_status.append(temp_dict)

            if count == 2:
                break

        return train_status

    def full_njt_dataset(self, password, username, station, direction):
        """Compile the schedule and departure vision to one json object."""
        departure = self.njt_departure(password, username, station)

        # update the schedule database
        self.update_njt_schedule(password, username, station, direction)
        schedule = self.get_njt_schedule()

        full_dataset = []

        departure_dict = {"departure_vision": departure}
        schedule_dict = {"schedule": schedule}

        full_dataset.append(departure_dict)
        full_dataset.append(schedule_dict)
        return full_dataset


class RssPlugin():
    """Rss feed plugin."""
    def __init__(self, feed, logger):
        self.feed = feed
        self.logger = logger

    def rss_feed(self):
        """Get rss data."""
        try:
            feed = feedparser.parse(self.feed)
            rss_data = feed.entries
            rss_json = [item.summary for item in rss_data]

            if len(rss_json) > 3:
                rand_nums = []
                while len(rand_nums) < 3:
                    temp = random.randint(0, len(rss_json) - 1)
                    if temp not in rand_nums:
                        rand_nums.append(temp)
                min_json = [rss_json[i] for i in rand_nums]
                return min_json
            else:
                return rss_json

        except Exception as e:
            self.logger.error(e)
            rss_json = {}
            return rss_json
