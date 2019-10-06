import requests
import os
import json

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

def test_city_search():
    city = 'Stowe'
    state = 'VT'
    days = '10'
    endpoint = 'http://api.weatherbit.io/v2.0/forecast/daily?'
    q_str = f'city={city},{state}&days={days}&key={API_KEY}'
    response = requests.get(endpoint+q_str)
    print('GET:', endpoint+q_str)
    print('STATUS CODE:', response.status_code)
    assert response.status_code == 200

    data = json.loads(response.text)
    print('DATA:', data)

if __name__ == '__main__':
    test_city_search()
