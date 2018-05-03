"""Config your personal smartmirror and setup for config.yml file."""

import yaml

print "-----------------------------------"
print "|                                 |"
print "|        Smart Mirror Setup       |"
print "|              v1.0.0             |"
print "-----------------------------------"

print "   "
print "The smart mirror uses the follow"
print "grid to display your desired plugins."
print " "
print "-----------------------------------"
print "|           Top Banner            |"
print "|                                 |"
print "-----------------------------------"
print "| Left   |               | R. Top |"
print "| Panel  |               |--------|"
print "|        |               | R.     |"
print "|        |               | Bottom |"
print "-----------------------------------"
print "|           Bottom Banner         |"
print "|                                 |"
print "-----------------------------------"
print " "


config_data = {}
plugin_store = {
	1: "greetings",
	2: "quotes",
	3: "python_tips",
	4: "reminders",
	5: "wunderground",
	6: "gmail",
	7: "placeholder",
	8: "time",
	9: "njt",
	10: "rss",
	11: "us_holidays",
	12: "random_facts"
}

# Helper Functions


def grid_setup_error(grid):
	"""Helper function to setup grids."""
	while True:
		try:
			choice = raw_input("Do you want to use the {g} (y/n)?: ".format(g=grid))
		except ValueError:
			print "Please enter y or n!"
			continue
		if choice in ("y", "n"):
			return choice
		else:
			print "Please enter y or n!"
			continue


def plugin_selection(location, start, end, plugin_store=plugin_store,):
	"""Helper function when selecting a plugin."""
	while True:
		try:
			plugin = int(raw_input("Please enter the plugin number (i.e. 1): "))
		except ValueError:
			print "Please enter a valid number"
			continue
		if plugin in range(start, end):
			config_data[location] = {plugin_store[plugin]: None}
			return plugin_store[plugin]
		else:
			print "Please enter a valid number"
			continue

print "Lets setup the Top Banner!"
print " "

tban = grid_setup_error("Top Banner")

if tban == 'y':
	print "These are the available plugins for the Top Banner:"
	print "1. Greetings"
	print "2. Quotes"
	print "3. Python Tips"
	print "4. Reminders"
	print ""

	plugin_selection("top_banner", 1, 5)


print "-----------------------------------"
print " "
print "Lets setup the Left Panel!"
print " "
lpanel = grid_setup_error("Left Panel")

if lpanel == 'y':
	print "These are the available plugins for the Left Panel:"
	print "5. Weather - Wunderground API required"
	print "6. Gmail"
	print "7. Place Holder"
	print " "
	_plugin = plugin_selection("left_panel", 5, 8)

	if _plugin == "wunderground":
		print ""
		print "Please sign up for the Wunderground API:"
		print "https://www.wunderground.com/weather/api"
		print ""
		api_key = raw_input('Please enter your wunderground API key: ')
		state = raw_input('Please enter your state (i.e. NJ) : ')
		zipcode = raw_input('Please enter your zipcode: ')
		config_data["left_panel"]["wunderground"] = {
			"api_key": api_key,
			"zipcode": zipcode,
			"state": state
		}

print "-----------------------------------"
print " "
print "Lets setup the Right Top Panel!"
print " "
rtop_panel = grid_setup_error("Right Top Panel")
if rtop_panel == 'y':
	print "Currently there is only one plugin for this panel"
	print " 8. Date and Time"
	print ""
	plugin_selection("right_top_panel", 8, 9)

print "-----------------------------------"
print " "
print "Lets setup the Right Bottom Panel!"
print " "
rbottom_panel = grid_setup_error("Right Bottom Panel")
if rbottom_panel == 'y':
	print "These are the available plugins for the Left Panel:"
	print "9. New Jesey Transit - NJT API required"
	print "10. Rss Feed"
	print " "
	right_plugin = plugin_selection("right_bottom_panel", 9, 11)

	if right_plugin == 'njt':
		print ""
		print "Please sign up for the New Jersey Transit API:"
		print "https://www.njtransit.com/mt/mt_servlet.srv?hdnPageAction=MTDevLoginTo"
		print ""

		njt_username = raw_input('Please enter your njt username: ')
		njt_password = raw_input('Please enter your njt password: ')
		train_station = raw_input('Please enter your train_station (please refer to the njt api documentation): ')

		config_data['right_bottom_panel']['njt'] = {
			"username": njt_username,
			"password": njt_password,
			"train_station": train_station
		}

	elif right_plugin == 'rss':
		rss_feed = raw_input('Please enter the url for the rss feed: ')
		config_data['right_bottom_panel']['rss'] = {
			"rss_feed": rss_feed
		}

print "-----------------------------------"
print " "
print "Lets setup the Bottom Banner!"
print " "
bottom_banner = grid_setup_error("Bottom Banner")
if bottom_banner == 'y':
	print "These are the available plugins for the Top Banner:"
	print "11. US Holidays"
	print "12. Random Facts"
	print ""

	plugin_selection("bottom_banner", 11, 13)

print ""
print "Saving your config to config.yml"
with open('config.yml', 'w') as output:
	yaml.dump(config_data, output, default_flow_style=False)

print "Excute the following command to start the smartmirror!"
print "./start.sh"