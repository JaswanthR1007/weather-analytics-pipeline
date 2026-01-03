import requests
import os

class WeatherAPIClient:
    def __init__(self):
        self.api_key = os.getenv('WEATHER_API_KEY')
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self, city):
        url = f"{self.base_url}/weather"
        params = {'q': city, 'appid': self.api_key}
        response = requests.get(url, params=params)
        return response.json()
