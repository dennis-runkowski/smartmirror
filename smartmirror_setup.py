"""Config your personal smartmirror and setup for config.yml file."""

import yaml
import sqlite3
import os

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
    4: "open_weather",
    5: "stock",
    6: "wunderground",
    7: "time",
    8: "njt",
    9: "rss",
    10: "us_holidays",
    11: "chuck_norris",
    12: "reminders"
}

# Helper Functions


def grid_setup_error(grid):
    """Helper function to setup grids."""
    while True:
        try:
            choice = raw_input(
                "Do you want to use the {g} (y/n)?: ".format(g=grid)
            )
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
            plugin = int(
                raw_input("Please enter the plugin number (i.e. 1): ")
            )
        except ValueError:
            print "Please enter a valid number"
            continue
        if plugin in range(start, end):
            config_data[location] = {plugin_store[plugin]: True}
            return plugin_store[plugin]
        else:
            print "Please enter a valid number"
            continue

# Create main db
if not os.path.exists('smartmirror/data_files/main.db'):
    print "creating"
    conn = sqlite3.connect('smartmirror/data_files/main.db')
    conn.close

# Create app secret key
key = os.urandom(24).encode('hex')
config_data["secret_key"] = key

print " "
test_env = grid_setup_error("testing configuration")
if test_env == 'y':
    config_data["environment"] = "testing"
else:
    config_data["environment"] = "production"

print "Lets setup the Top Banner!"
print " "

tban = grid_setup_error("Top Banner")

if tban == 'y':
    print "These are the available plugins for the Top Banner:"
    print "1. Greetings"
    print "2. Quotes"
    print "3. Python Tips"
    print ""

    plugin_selection("top_banner", 1, 4)


print "-----------------------------------"
print " "
print "Lets setup the Left Panel!"
print " "
lpanel = grid_setup_error("Left Panel")

if lpanel == 'y':
    print "These are the available plugins for the Left Panel:"
    print "4. Weather - Open Weather"
    print "5. Stock"
    print "6. Weather - Wunderground API required (deprecated)"
    print " "
    _plugin = plugin_selection("left_panel", 4, 7)

    if _plugin == "open_weather":
        print "You need an open weather api key and your location (lon/lat)."
        print "You can use this link to find your city and sign up."
        print "https://openweathermap.org/"
        lon = raw_input("Please enter your lon:")
        lat = raw_input("Please enter your lat:")
        api_key = raw_input("Please enter your open weather api key:")
        forecast_type = raw_input(
            "Do you want an hourly or daily forecast (hourly/daily):")
        units = raw_input("Do you want to use imperial or metric units (imperial/metric):")
        config_data["left_panel"]["open_weather"] = {
            "lon": lon,
            "lat": lat,
            "api_key": api_key,
            "units": units,
            "type": forecast_type
        }
    elif _plugin == "wunderground":
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
    elif _plugin == "stock":
        print ""
        print "Please sign up for the Alpha Advantage API:"
        print "https://www.alphavantage.co/support/#api-key"
        print ""
        api_key = raw_input('Please enter your alphavantage API key: ')
        tickers = raw_input(
            'Please enter the tickers you wish to follow (i.e. AAPL T AXP ..):'
        )
        tickers_list = tickers.split(' ')
        print tickers_list
        config_data["left_panel"]["stock"] = {
            "api_key": api_key,
            "tickers": tickers_list
        }


print "-----------------------------------"
print " "
print "Lets setup the Right Top Panel!"
print " "
rtop_panel = grid_setup_error("Right Top Panel")
if rtop_panel == 'y':
    print "Currently there is only one plugin for this panel"
    print " 7. Date and Time"
    print ""
    plugin_selection("right_top_panel", 7, 8)

print "-----------------------------------"
print " "
print "Lets setup the Right Bottom Panel!"
print " "
rbottom_panel = grid_setup_error("Right Bottom Panel")
if rbottom_panel == 'y':
    print "These are the available plugins for the Left Panel:"
    print "8. New Jesey Transit - NJT API required"
    print "9. Rss Feed"
    print " "
    right_plugin = plugin_selection("right_bottom_panel", 8, 10)

    if right_plugin == 'njt':
        print ""
        print "Please sign up for the New Jersey Transit API:"
        print "https://www.njtransit.com/mt/mt_servlet.srv?hdnPageAction=MTDevLoginTo"
        print ""

        njt_username = raw_input('Please enter your njt username: ')
        njt_password = raw_input('Please enter your njt password: ')
        train_station = raw_input(
            'Please enter your train_station (please refer to the njt api documentation): '
        )

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
    print "10. US Holidays"
    print "11. Chuck Norris Jokes"
    print "12. Reminders"
    print ""

    plugin_selection("bottom_banner", 10, 13)

print ""
print "Saving your config to config.yml"
with open('config.yml', 'w') as output:
    yaml.dump(config_data, output, default_flow_style=False)

print "Completed!"
