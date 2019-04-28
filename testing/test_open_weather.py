import os
import sys
import logging
import pprint
sys.path.append("/home/dennis_ubuntu/GitHub/smartmirror/smartmirror")
from plugins.left_panel import OpenWeather

pp = pprint.PrettyPrinter(indent=4)

test = OpenWeather(
    lat='33.5499',
    lon='-79.0431',
    api_key='',
    logger=logging
)
pp.pprint(test.current_weather())

pp.pprint(test.forecast('hourly'))

pp.pprint(test.forecast('daily'))