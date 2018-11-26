from ..extensions import db
from datetime import datetime, date


class NJTModel(db.Model):
    __tablename__ = 'njt'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(80))
    direction = db.Column(db.String(80))
    created_date = db.Column(db.Date, default=date.today())

    def __init__(self, time, direction, created_date):
        self.time = time
        self.direction = direction
        self.created_date = created_date

    def json(self):
        return {'time': self.time}

    @classmethod
    def get_last_update(cls):
        time_stamp = cls.query.limit(1).all()
        if time_stamp:
            return time_stamp[0].created_date
        else:
            return False

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def delete_all(cls):
        cls.query.delete()

    @classmethod
    def query_all(cls):
        schedule_time = []
        for _row in cls.query.all():
            date_obj = datetime.strptime(_row.time, '%d-%b-%Y %I:%M:%S %p')
            if datetime.now() < date_obj:
                schedule_time.append(date_obj)
        if len(schedule_time) >= 1:
            recent = [datetime.strftime(t, '%I:%M %p') for t in schedule_time]

            return recent

        else:
            """Return no data if there is no upcoming trains."""
            recent = []
            return recent


class APIlimit(db.Model):
    __tablename__ = 'api_limit'

    id = db.Column(db.Integer, primary_key=True)
    api_name = db.Column(db.String(80), unique=True)
    request_count = db.Column(db.Integer)

    def __init__(self, api_name, request_count):
        self.api_name = api_name
        self.request_count = request_count

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_counter(self):
        counter = self.query.filter_by(api_name=self.api_name).first()
        counter.request_count += 1
        db.session.add(counter)
        db.session.commit()

    def reset_counter(self):
        reset = self.query.filter_by(api_name=self.api_name).first()
        reset.request_count = 0
        db.session.add(reset)
        db.session.commit()

    @classmethod
    def get_row(cls, api_name):
        count = cls.query.filter_by(api_name=api_name).first()
        if not count:
            return None
        else:
            return count


class ReminderModel(db.Model):
    """
    This is a SQL model for storing user defined reminders.

    Attributes:
        reminder_date (datetime): Reminder start date.
        comment (str): The text for the reminder.
        duration (datetime): Reminder end date.
    """

    __tablename__ = 'reminders'

    id = db.Column(db.Integer, primary_key=True)
    reminder_date = db.Column(db.DateTime)
    comment = db.Column(db.String(160))
    duration = db.Column(db.DateTime)

    def __init__(self, reminder_date, comment, duration):
        """
        The constructor for the ReminderModel class.

        Parameters:
            reminder_date (datetime): Reminder start date.
            comment (str): The text for the reminder.
            duration (datetime): Reminder end date.
        """
        self.reminder_date = reminder_date
        self.comment = comment
        self.duration = duration

    def save_to_db(self):
        """Save reminder data to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Delete reminder data from the database."""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_reminders(cls, current_date):
        """
        Class method to get the reminders during at a point in time.

        Parameters:
            current_date (datetime): The current datetime (%m-%d-%y:%h%s%m).
        Returns:
            reminder_list: A list containing the current reminders.
        """
        reminder = cls.query.filter(
            cls.reminder_date <= current_date).filter(
            cls.duration >= current_date
        )
        return reminder

    @classmethod
    def get_all_reminders(cls):
        """
        Class method to get all the reminders in the database.

        Returns:
            all_reminders: list of all the reminders.
        """
        all_reminders = cls.query.all()
        return all_reminders

    @classmethod
    def find_by_id(cls, _id):
        """
        Class method to find reminders from the database.

        Parameters:
            id (str): The id for the reminder.
        """
        return cls.query.filter_by(id=_id).first()
