# define helper functions if needed
# and put them in `imdb_helper_functions` module.
# you can import them and use here like that:
#from imdb_helper_functions import helper_function_example

import urllib.request
from bs4 import BeautifulSoup
import requests
import time
from module1 import film_description
from module1 import actor_data
import csv

BASE_URL="https://www.imdb.com"
# import pandas as pd

def get_actors_by_movie_soup(cast_page_soup, num_of_actors_limit=None):

    #нашли все заголовки с актерами
    all_cast_headers =  cast_page_soup.find_all("tr", attrs={'class':
                                       ('odd', 'even')})

    #ну крч в каждом заголовке с актером берем юрл и имя и херачим списокег
    cast = [(all_cast_headers[i].find('img')['alt'], urllib.parse.urljoin(BASE_URL, all_cast_headers[i].find('a')['href']))
              for i in range(len(all_cast_headers))]
    
    
    if num_of_actors_limit == None:
        return cast
    elif num_of_actors_limit >= len(cast):
        return cast
    else: 
        return  cast[:num_of_actors_limit]


def get_movies_by_actor_soup(actor_page_soup, num_of_movies_limit=None):

    full_feat =  ('TV Series', 'Short', 'Video Game', 
                   'Video short', 'Video', 'TV Movie', 
                   'TV Mini Series', 'TV Series short', 'TV Special', 
                   'announced', 'completed', 'voice', 'uncredited')

    movie_headers_all = actor_page_soup.find_all('div', 
                                               attrs = {'class': 'filmo-category-section'})
    movies_soup = movie_headers_all[0].find_all('div', 
                                               attrs = {'class': ('filmo-row odd', 'filmo-row even')})
    
    movies = [(movies_soup[i].find('a').text, urllib.parse.urljoin(BASE_URL, movies_soup[i].find('a')['href']))
               for i in range(len(movies_soup))
               if all(x not in movies_soup[i].text for x in full_feat) and (len(movies_soup[i].find_all('a', attrs = {'class': 'in_production'})))==0]
    
    if num_of_movies_limit == None:
        return movies
    elif num_of_movies_limit >= len(movies):
        return movies
    else: 
        return movies[:num_of_movies_limit]


def get_movie_distance(actor_start_url, actor_end_url, num_of_actors_limit=5, num_of_movies_limit=5):
    
    if actor_start_url[8:11] == 'imd':
        actor_start_url = 'https://' + 'www.' + actor_start_url[8:]
    if actor_end_url[8:11] == 'imd':
        actor_end_url = 'https://' + 'www.' + actor_end_url[8:]

    actor_start = actor_data(actor_start_url) 
    actor_end = actor_data(actor_end_url)

    # get list of actors with different levels
    distance = 1
    
    distance_limit = 3
    
    actor_cash = [actor_start]
    
    for x in range(distance_limit):
        movies_cash = []
        
        for actor_name, actor_url in actor_cash:
        
            headers = {'Accept-Language': 'en', 'X-FORWARDED-FOR': '2.21.184.0'}
            response = requests.get(actor_url, headers=headers)
            actor_page_soup = BeautifulSoup(response.content, 'html.parser')

            movies_actor = get_movies_by_actor_soup(actor_page_soup, num_of_movies_limit)
            for mov_act in movies_actor:
                if mov_act not in movies_cash:
                    movies_cash.append(mov_act)
        print(movies_cash)
        actor_cash = []
        
        for movie_name, movie_url in movies_cash:
        
            headers = {'Accept-Language': 'en',
                   'X-FORWARDED-FOR': '2.21.184.0'}

            response = requests.get(movie_url + 'fullcredits/', headers=headers)
        
            cast_page_soup = BeautifulSoup(response.content, 'html.parser')
            actor_movies = get_actors_by_movie_soup(cast_page_soup, num_of_actors_limit)# + 'fullcredits/'
            for ac_mov in actor_movies:
                if ac_mov not in actor_cash:
                     actor_cash.append(ac_mov)
            if actor_end in actor_cash:
                return distance
            print(actor_cash)
        distance = distance + 1
    return -1


def get_movie_descriptions_by_actor_soup(actor_page_soup):
    description_of_film = []
    nameFilm = []
    movies_by_actor = get_movies_by_actor_soup(actor_page_soup)
    for film in movies_by_actor:
        nameFilm.append(film[0])
        description_of_film.append(str(film_description(film[1])))

        #замена плохого символа, так как иначе невозможно записать в файл
        description_of_film[-1] = description_of_film[-1].replace('\xf6', 'o') 
        description_of_film[-1] = description_of_film[-1].replace('\xe9', 'e') 
        description_of_film[-1] = description_of_film[-1].replace('\xed', 'i') 

    file = open('description.txt', 'w', newline='\n')
    for dec in description_of_film:
        file.writelines(dec + '\n')

    file.close()

    return description_of_film





