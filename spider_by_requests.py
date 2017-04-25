# -*- coding: utf-8 -*-
from douban import DouBan
from mysql import Mysql


class SaveData:
    def __init__(self):
        self._douban = DouBan()
        self._mysql = Mysql()
        self._movie_all_pages = []
        self._movie_all_types = []

    def _get_data(self):
        movie_types = []
        for page_number in range(25):
            self._douban.get_html_page_content(page_number)
            self._douban.get_movies()
            self._douban.parse_movies_from_html()
            movies_with_id = ("\"),\n (".join([str(index+25*page_number) + ", \"" + "\",\"".join(movie[:-1])
                                              for index, movie in enumerate(self._douban.get_movies(), 1)]))

            one_page_movies = ("".join(["(", movies_with_id, "\")"]))
            self._movie_all_pages.append(one_page_movies)

            for movie in self._douban.get_movies():
                types = movie[-1].split(",")
                movie_types.extend(list(zip([movie[0]]*len(types), types)))

        for index, t in enumerate(movie_types, 1):
            t_list = list(t)
            t_list.insert(0, index)
            self._movie_all_types.append(str(t_list).replace("[", "(").replace("]", ")"))

    def save_data_to_file(self):
        insert_movies = "DELETE from movies;\n" \
                        "INSERT INTO `movies` " \
                        "(`id`, `name`, `directors`, `stars`, `country`, `year`, `link`, `description`)\n"

        insert_types = "\nDELETE from movie_types;\n" \
                       "INSERT INTO `movie_types` " \
                       "(`id`, `movie_name`, `movie_type`)\n"

        self._get_data()

        ddl_movies = ("".join([insert_movies, "VALUES\n ", ",\n ".join(self._movie_all_pages), ";"]))
        ddl_types = "".join([insert_types, "VALUES\n", ",\n ".join(self._movie_all_types), ";\n"])

        with open("db/migration/V__init_tables.sql", "w+", encoding='utf-8') as f:
            f.write(ddl_movies)
            f.write(ddl_types)

    def save_data_to_db(self):
        with open("db/migration/V201704242121__add_tables.sql", "r") as f:
            self._mysql.migrate(f.read())
        with open("db/migration/V__init_tables.sql", "r", encoding="utf-8") as f:
            self._mysql.migrate(f.read())
        self._mysql.close()

if __name__ == "__main__":
    data = SaveData()
    data.save_data_to_file()
    data.save_data_to_db()
    print("Done")
