"""View for testing."""
from flask import Blueprint, jsonify
from datetime import datetime
import sys

sys.path.append('../../')

from smartmirror.models.models import ReminderModel
from smartmirror.extensions import db

test = Blueprint('test', __name__, url_prefix='/')


@test.route('/')
def index():
	start_date = datetime.strptime("2018-11-17 05:00:00", '%Y-%m-%d %H:%M:%S')
	end_date = datetime.strptime("2018-11-17 06:00:00", '%Y-%m-%d %H:%M:%S')
	data = ReminderModel(start_date, 'This should Hit', end_date)
	data.save_to_db()

	test_date = datetime.strptime("2018-11-17 05:30:00", '%Y-%m-%d %H:%M:%S')
	res = ReminderModel.get_reminders(test_date)
	for i in res:
		print i.comment
	return jsonify("Hello World")