#!/usr/bin/python -u

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from datetime import datetime, tzinfo, timedelta
import httplib as http
import sys
import json



class customtz(tzinfo):
	def __init__(self, offset=(-8*60*60), name=None):
		self.offset = timedelta(seconds=offset)
		self.name = name or self.__class__.__name__
	def utcoffset(self, dt):
		return self.offset
	def dst(self, dt):
		return timedelta(0)
	def tzname(self, dt):
		return self.name

class thermostat(object):
	pins = {}
	
	def __init__(self):
		...

	

class thermostatEvent(object):
	timezone = customtz(name="pst")
	logLine = "%s,%s,%s,%s,%s\n"

	def __init__(self, power, weather_json):
		self.power = power
		self.datetime = datetime.now(self.timezone).replace(microsecond=0)
		self.weather_json = weather_json
		if (6 <= self.datetime.hour < 19):
			self.settemp = 68
		else:
			self.settemp = 65

	@classmethod
	def logheader(cls, file):
		file.write("initializing at: %s\n" % datetime.now(cls.timezone).replace(microsecond=0).isoformat())
		file.write(cls.logLine % ("Value", "Time", "Target Temp", "Exterior Temp", "Weather"))
		file.flush()

	def log(self, file):
		file.write(self.logLine % (
			self.power,
			self.datetime.isoformat(),
			self.settemp,
			openweather.temp(self.weather_json),
			"'%s'" % json.dumps(self.weather_json)
		))
		file.flush()


class openweather(object):
	host = "api.openweathermap.org"

	def __init__(self, lat, lon, api_key, units="imperial"):
		self.path = "/data/2.5/weather?lat=%s&lon=%s&appid=%s&units=%s" % (lat, lon, api_key, units)
		self.cached = None
	
	def get(self):
		if (self.cached and datetime.now() - openweather.timestamp(self.cached) < timedelta(minutes=30)):
			return self.cached
		conn = http.HTTPSConnection(self.host)
		try:
			conn.request("GET", self.path)
			response = conn.getresponse()
			if (200 <= response.status < 300):
				self.cached = json.loads(response.read())
				return self.cached
			else:
				print (response.status + " " + response.reason)
				return self.cached
		finally:
			conn.close()
	
	@staticmethod
	def timestamp(weather_json):
		return datetime.fromtimestamp(weather_json["dt"])

	@staticmethod
	def temp(weather_json):
		return weather_json["main"]["temp"]


def main():
	weatherapi = openweather(47.7127, -122.3339, "079ef2f15d85b4c7029c04822092addf")
	input_pin = "P8_10"
	lastEvent = thermostatEvent(-1, weatherapi.get())

	GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	try:
		with open("/home/root/furnace_v2.log", "w") as f:
			thermostatEvent.logheader(f)
			while (True):
				event = thermostatEvent(GPIO.input(input_pin), weatherapi.get())
				if (lastEvent.power != event.power):
					lastEvent = event
				event.log(f)
				GPIO.wait_for_edge(input_pin, GPIO.BOTH)
	except Exception as e:
		print("An exception has halted the logger %s" % e)
		raise
	finally:
		print("Closing!")
		GPIO.cleanup()

if __name__ == '__main__':
	sys.exit(main() or 0)
