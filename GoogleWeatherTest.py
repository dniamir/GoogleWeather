from GoogleWeather import GoogleWeatherAPI

region = 'Redwood City'

# Instantiate class and import data
google_weather = GoogleWeatherAPI()
data = google_weather.GetDataFromRegion(region)

# Create banner
banner = '=' * 40

# print data
print('Weather for: %s' % data['region'])
print('Now: %s' % data['dayhour'])
print('Temperature now: %i C' % data['temp_c'])
print('Description: %s' % data['weather_now'])
print('Chance of Precipitation: %s' % data['precipitation'])
print('Humidity: %i PerRelHumid' % data['humidity'])
print('Wind: %i MPH' % data['wind'])
print('Next days:')
for dayweather in data['next_days']:
    print('%s %s %s' % (banner, dayweather['name'], banner))
    print('Description: %s' % dayweather['weather'])
    print(f'Max temperature: %i C' % dayweather['max_temp_c'])
    print(f'Min temperature: %i C' % dayweather['min_temp_c'])
