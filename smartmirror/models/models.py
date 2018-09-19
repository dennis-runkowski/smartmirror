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
		reset.request_count -= 1
		db.session.add(reset)
		db.session.commit()

	@classmethod
	def get_row(cls, api_name):
		count = cls.query.filter_by(api_name=api_name).first()
		if not count:
			return None
		else:
			return count


