# -*- coding: utf-8 -*-
from lxml import html
import requests


def get_html_page_content(pages_number):
    url = "".join(["https://movie.douban.com/top250?start=", str(pages_number), "&filter="])
    page = requests.get(url).content
    tree = html.fromstring(page)
    movie_contents = tree.xpath("./body/div[@id='wrapper']/div[@id='content']//div[@class='info']")
    return movie_contents


def get_movies(movie_contents):
    movies = []

    for movieContent in movie_contents:
        movie = []
        movie_address = movieContent.xpath("./div[@class='hd']/a")[0].attrib['href']
        movie.append(movie_address)

        movie_name = movieContent.find("./div[@class='hd']/a/span").text
        movie.append(movie_name)

        movie_details = [star.xpath("string()").strip() for star in movieContent.xpath("./div[@class='bd']//p")]
        movie_descriptions = movie_details[1]
        movie.append(movie_descriptions)

        movie_staff_type = movie_details[0].split("\n")

        movie_year_local_type = movie_staff_type[-1].strip().split("/")
        movie_year = movie_year_local_type[0].strip()
        movie_location = movie_year_local_type[1].strip()
        movie_type = [t.strip() for t in movie_year_local_type[2].split()]
        movie.append(movie_year)
        movie.append(movie_location)
        movie.append(movie_type)

        movie_staff = [ds.split(":")[-1].split("/") for ds in movie_staff_type[0].split("\xa0\xa0\xa0")]
        movie_directors = [director.strip() for director in movie_staff[0]]
        movie.append(movie_directors)
        movie_stars = [star.strip() for star in movie_staff[1]]
        movie.append(movie_stars)
        movies.append(movie)
    return movies

if __name__ == "__main__":
    for page_number in range(25):
        for movie in get_movies(get_html_page_content(page_number)):
            print(movie)
