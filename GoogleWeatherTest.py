from GoogleWeather import GoogleWeatherAPI

google_weather = GoogleWeatherAPI()

region = "New York"
data = google_weather.GetDataFromRegion(region)

# print data
print("Weather for:", data["region"])
print("Now:", data["dayhour"])
print(f"Temperature now: {data['temp_c']}°C")
print("Description:", data['weather_now'])
print("Precipitation:", data["precipitation"])
print("Humidity:", data["humidity"])
print("Wind:", data["wind"])
print("Next days:")
for dayweather in data["next_days"]:
  print("=" * 40, dayweather["name"], "=" * 40)
  print("Description:", dayweather["weather"])
  print(f"Max temperature: {dayweather['max_temp_c']}°C")
  print(f"Min temperature: {dayweather['min_temp_c']}°C")