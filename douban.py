# -*- coding: utf-8 -*-
from lxml import html
import requests


class DouBan:

    def __init__(self):
        self._movie_contents = None
        self._movies = None

    def get_movies(self):
        return self._movies

    def get_html_page_content(self, pages_number):
        self._movie_contents = []
        url = "".join(["https://movie.douban.com/top250?start=", str(pages_number), "&filter="])
        page = requests.get(url).content
        tree = html.fromstring(page)
        self._movie_contents = tree.xpath("./body/div[@id='wrapper']/div[@id='content']//div[@class='info']")

    def parse_movies_from_html(self):
        self._movies = []
        for movieContent in self._movie_contents:
            movie = []
            movie_name = movieContent.find("./div[@class='hd']/a/span").text
            movie.append(movie_name)

            movie_details = [star.xpath("string()").strip() for star in movieContent.xpath("./div[@class='bd']//p")]

            movie_staff_type = movie_details[0].split("\n")

            movie_year_local_type = movie_staff_type[-1].strip().split("/")

            movie_staff = [ds.split(":")[-1].split("/") for ds in movie_staff_type[0].split("\xa0\xa0\xa0")]
            movie_directors = ",".join([director.strip() for director in movie_staff[0]])
            movie.append(movie_directors)
            movie_stars = ",".join([star.strip() for star in movie_staff[1]])
            movie.append(movie_stars)

            movie_year = movie_year_local_type[0].strip()
            movie_location = movie_year_local_type[1].strip()
            movie_type = ",".join([t.strip() for t in movie_year_local_type[2].split()])
            movie.append(movie_location)
            movie.append(movie_year)

            movie_address = movieContent.xpath("./div[@class='hd']/a")[0].attrib['href']
            movie.append(movie_address)

            movie_descriptions = movie_details[1]
            movie.append(movie_descriptions.strip())
            movie.append(movie_type)

            self._movies.append(movie)


if __name__ == "__main__":
    douban = DouBan()
    movie_types = []
    movie_all_pages = []
    insert_movies = "DELETE from movies;\n" \
                    "INSERT INTO `movies` " \
                    "(`id`, `name`, `directors`, `stars`, `country`, `year`, `link`, `description`)\n"

    insert_types = "\nDELETE from movie_types;\n" \
                   "INSERT INTO `movie_types` " \
                   "(`id`, `movie_name`, `movie_type`)\n"

    for page_number in range(25):
        douban.get_html_page_content(page_number)
        douban.parse_movies_from_html()
        movies_with_id = ("\"),\n (".join([str(index+25*page_number) + ", \"" + "\",\"".join(movie[:-1])
                                          for index, movie in enumerate(douban.get_movies(), 1)]))

        one_page_movies = ("".join(["(", movies_with_id, "\")"]))
        movie_all_pages.append(one_page_movies)

        for movie in douban.get_movies():
            types = movie[-1].split(",")
            movie_types.extend(list(zip([movie[0]]*len(types), types)))

    ddl_movies = ("".join([insert_movies, "VALUES\n ", ",\n ".join(movie_all_pages), ";"]))

    types_with_id = []
    for index, t in enumerate(movie_types, 1):
        t_list = list(t)
        t_list.insert(0, index)
        types_with_id.append(str(t_list).replace("[", "(").replace("]", ")"))
    types_with_id = ",\n ".join(types_with_id)

    ddl_types = "".join([insert_types, "VALUES\n", types_with_id, ";\n"])

    with open("db/migration/V__init_tables.sql", "w+", encoding='utf-8') as f:
        f.write(ddl_movies)
        f.write(ddl_types)




