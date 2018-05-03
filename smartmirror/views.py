from flask import Blueprint, request, jsonify, render_template
from flask import current_app as app
from extensions import cache
from datetime import datetime, time
from plugins import top_banner

# Blue print for the main display
blueprint = Blueprint(
	'smartmirror',
	__name__,
	template_folder='templates',
	static_folder='static'
)
# Blueprint for the right top panel
right_top = Blueprint(
	'right_top_panel',
	__name__,
	template_folder='templates',
	static_folder='static'
)
# Blueprint for the Top Banner section
top_banner_blueprint = Blueprint(
	'top_banner',
	__name__,
	template_folder='template',
	static_folder='static'
)


@blueprint.route('/', methods=['GET'])
def smartmirror():
	"""Main Smart Mirror Template."""
	# Top Banner Template setup
	if app.config.get('top_banner'):
		top_banner_plugin = app.config.get('top_banner')
		top_banner = 'top_banner/{t}.html'.format(t=top_banner_plugin.keys()[0])
	else:
		top_banner = False

	# Right Top Template setup
	if app.config.get('right_top_panel'):
		right_top_plugin = app.config.get('right_top_panel')
		right_top_panel = 'right_top/{t}.html'.format(t=right_top_plugin.keys()[0])
	else:
		right_top_panel = False
	return render_template(
		'main.html',
		right_top_panel=right_top_panel,
		top_banner=top_banner
	)

##########################################################
"""
This Section contains all the endpoints for the Top Banner
Currently the only plugins available are the following:
	-Greetings
	-Quotes
	-Python Tips
	-Reminders
"""
###########################################################


@top_banner_blueprint.route('/top_banner', methods=['GET', 'POST'])
def top_banner_endpoint():
	"""Endpoint for the Top Banner."""
	data = top_banner.TopBanner()
	tb_config = app.config.get('top_banner').keys()[0]

	if tb_config == 'greetings':
		return jsonify(data.greetings())
	elif tb_config == 'quotes':
		return jsonify(data.quotes())
	else:
		return jsonify({"Error": "No plugins selected"})


# @blueprint.route('/trains', methods=['GET'])
# def trains():
# 	data = njt.trains()
# 	test = data.schedule()
# 	return jsonify(test)


###########################################################
"""
This Section contains all the endpoints for the right top panel
Currently the only plugins available are the following:
	-Date and Time
"""
###########################################################


@right_top.route('/date_time', methods=['GET', 'POST'])
@cache.cached(timeout=10)
def date_time():
	"""Route for the current time and data."""
	data = {}
	date_time = datetime.now().strftime("%A, %B %d, %Y # %I:%M:%S %p")
	dt_split = date_time.split("#")
	data["date"] = dt_split[0]
	data["time"] = dt_split[1]

	return jsonify(data)


