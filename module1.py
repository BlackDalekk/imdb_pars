import urllib.request
from bs4 import BeautifulSoup
import requests

def actor_data(url):
        headers = {'Accept-Language': 'en',
          'X-FORWARDED-FOR': '2.21.184.0'}
        actor_request = requests.get(url, headers=headers)
        actor_soup = BeautifulSoup(actor_request.text, 'html.parser')
        actor_soup = actor_soup.find('span', attrs={'class': 'itemprop'})
        actor_name = actor_soup.text
        actor_url = url
        return (actor_name, actor_url)

def film_description(url):
        headers = {'Accept-Language': 'en',
          'X-FORWARDED-FOR': '2.21.184.0'}
        film_request = requests.get(url, headers=headers)
        film_soup = BeautifulSoup(film_request.text, 'html.parser')
        film_soup = film_soup.find('span', attrs={'class': 'sc-16ede01-2 gXUyNh'})
        description_of_film = film_soup.text
        return description_of_film
