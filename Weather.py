import requests
import toml

config = toml.load('config.toml')

api_key_weather = config['api_key_weather']


def get_temp(city, ):
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key_weather}&units=kelvin"

    response = requests.get(weather_url).json()

    temp = response['main']['temp']
    temp_feelslike = response['main']['feels_like']
    pressure = response['main']['pressure']
    humidity = response['main']['humidity']
    maximum = response['main']['temp_max']
    minimum = response['main']['temp_min']

    return f'/me : Temperature in {city}: {temp}K (feels like {temp_feelslike}K) BatChest // \
        Humidity in {city}: {humidity}% 💦 // Pressure in {city}: {pressure}hPa 🗜 4Head // Max. Temp in {city}: \
        {maximum}K and Min. Temp in {city}: {minimum}K forsenScoots'

def main():
    get_temp('berlin')


if __name__ == '__main__':
    main()