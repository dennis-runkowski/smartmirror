"""This class contains all the plugins for the right top banner."""
from datetime import datetime


class DateTime():
	def __init__(self, logger):
		"""Setting up logger."""
		self.logger = logger

	def date_time(self):
		"""Route for the current time and data."""
		data = {}
		date_time = datetime.now().strftime("%A, %B %d, %Y # %I:%M:%S %p")
		dt_split = date_time.split("#")
		data["date"] = dt_split[0]
		data["time"] = dt_split[1]
		self.logger.debug("DateTime - %s", data)

		return data
