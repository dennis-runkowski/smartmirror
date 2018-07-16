"""This class contains all the plugins for the top banner."""
from datetime import datetime, time
import json
import random


class GreetingPlugin():
	def __init__(self):
		pass

	def greetings(self):
		"""Plugin to show greetings throughout the day."""
		current_time = datetime.now().time()

		if time(5, 00) <= current_time <= time(12, 00):
			return {"greeting": "Good Morning!"}
		elif time(12, 00) <= current_time <= time(17, 00):
			return {"greeting": "Good Afternoon!"}
		elif time(17, 00) <= current_time <= time(21, 00):
			return {"greeting": "Good Evening!"}
		else:
			return {"greeting": "Goodnight!"}


class QuotePlugin():
	def __init__(self):
		pass

	def quotes(self):
		"""Plugin that gets random famous quotes."""
		with open('smartmirror/data_files/quotes.json', 'r') as data:
			quotes = json.load(data)
			data.close()

		random_number = random.randint(0, 1640)
		return quotes[random_number]


class PythonTipPlugin():
	def __init__(self):
		pass

	def python_tips(self):
		"""Plugin that gets random python tips."""
		with open('smartmirror/data_files/python_tips.json', 'r') as data:
			py_tips = json.load(data)
			data.close()

		random_number = random.randint(0, 44)
		return py_tips[random_number]
