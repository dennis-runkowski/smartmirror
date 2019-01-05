import os
import sys
import logging
sys.path.append("/home/dennis_ubuntu/GitHub/smartmirror/smartmirror")
from plugins.left_panel import OpenWeather

test = OpenWeather(
    units="metric",
    lat='40.812',
    lon='-74.1243',
    api_key='139cb4d088ba4fff72d34034fdb367b9',
    logger=logging
)
print test.current_weather()