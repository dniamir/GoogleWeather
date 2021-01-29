"""Simple class to record and save data from Google Weather
Based on code from the link below:

https://www.thepythoncode.com/article/extract-weather-data-python

"""
from bs4 import BeautifulSoup as bs
import requests


class GoogleWeatherAPI(object):
	"""Simple class to record and save data from Google Weather

	Data is saved as a class variable. The highest level in this dictionary is the
	region name. The next level down is also a dictionary with all recently saved
	data"""
	USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
	LANGUAGE = "en-US,en;q=0.5"
	URL = "https://www.google.com/search?lr=lang_en&ie=UTF-8&q=weather"

	def __init__(self):
		self.data = {}

	def FarenheitToCelsius(self, temperature_f):
		"""Convert temperature from F to C

		Args:
		temperature_f: float. Temperature in Farenheight

		Outputs:
		temperature_c: float. Temperature in Celsius
		"""
		temperature_c = (temperature_f - 32) * 5. / 9
		return temperature_c

	def CelsiusToFarenheit(self, temperature_c):
		"""Convert temperature from C to F

		Args:
		temperature_f: float. Temperature in Farenheight

		Outputs:
		temperature_c: float. Temperature in Celsius
		"""
		temperature_f = temperature_c * 9. / 5 + 32
		return temperature_f

	def GetDataFromRegion(self, region='San Francisco'):
		"""Read data from google weather to """

		# Update URL
		new_region = region.replace(' ', '+')
		url_region = '%s+%s' % (self.URL, new_region)

		# Read data from URL
		session = requests.Session()
		session.headers['User-Agent'] = self.USER_AGENT
		session.headers['Accept-Language'] = self.LANGUAGE
		session.headers['Content-Language'] = self.LANGUAGE
		html = session.get(url_region)
		soup = bs(html.text, "html.parser")

		# Store data in dictionary
		data_region = {}
		data_region['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
		data_region['temp_f'] = float(soup.find("span", attrs={"id": "wob_tm"}).text)
		data_region['temp_c'] = self.FarenheitToCelsius(data_region['temp_f'])
		data_region['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
		data_region['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
		data_region['precipitation'] = soup.find("span", attrs={"id": "wob_pp"}).text
		data_region['humidity'] = float(
			soup.find("span", attrs={"id": "wob_hm"}).text.replace('%', ''))  # % Relative Himidity
		data_region['wind'] = float(soup.find("span", attrs={"id": "wob_ws"}).text.replace('mph', ''))  # MPH

		# Store data from rest of the week
		next_days = []
		days = soup.find("div", attrs={"id": "wob_dp"})
		for day in days.findAll("div", attrs={"class": "wob_df"}):
			day_name = day.find("div").attrs['aria-label']
			weather = day.find("img").attrs["alt"]
			temp = day.findAll("span", {"class": "wob_t"})

			max_temp_f = float(temp[0].text)
			max_temp_c = float(temp[1].text)
			min_temp_f = float(temp[2].text)
			min_temp_c = float(temp[3].text)

			next_days.append({'name': day_name,
			                  'weather': weather,
			                  'max_temp_c': max_temp_c,
			                  'max_temp_f': max_temp_f,
			                  'min_temp_c': min_temp_c,
			                  'min_temp_f': min_temp_f})
		# append to result
		data_region['next_days'] = next_days

		# Save data to class
		self.data[region] = data_region

		return data_region
