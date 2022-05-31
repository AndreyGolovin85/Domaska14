import sqlite3
from collections import Counter
from sqlite3 import Error
import setting


def creat_connection(path):
    """
    Функция для подключения к базе данных
    :param path:
    :return:
    """
    try:
        with sqlite3.connect(path) as connection:
            cursor = connection.cursor()
            print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return cursor


def search_movie_by_name(cursor, name_movie) -> dict:
    """
    Функция для вывода фильма из базы по названию
    :param cursor:
    :param name_movie: str
    :return: dict
    """
    query = """
            SELECT title, country, release_year, listed_in, description, MAX(release_year)
            FROM netflix
            WHERE title = ?
            """
    cursor.execute(query, (name_movie, ))
    movie_info = cursor.fetchall()[0]
    movie_info_dict = {
        "title": movie_info[0],
        "country": movie_info[1],
        "release_year": movie_info[2],
        "genre": movie_info[3],
        "description": movie_info[4]
    }
    return movie_info_dict


def search_movie_by_range_year(cursor, year_1, year_2) -> list:
    """
    Функция принимает 2 числа(годы) и выводит из базы фильмы в диапазоне годов
    Установлено ограничение на количество в 100 фильмов
    :param cursor:
    :param year_1: int
    :param year_2: int
    :return: list
    """
    json_format = []
    query = f"""
                SELECT title, release_year
                FROM netflix
                WHERE release_year BETWEEN {year_1} AND {year_2}
                LIMIT 100
                """
    cursor.execute(query)
    movie_list = cursor.fetchall()
    for movie in movie_list:
        json_format.append({"title": movie[0], "release_year": movie[1]}, )

    return json_format


def search_movie_by_rating(cursor, rating) -> list:
    """
    Функция выбирает фильмы из базы данных по рейтингу
    :param cursor:
    :param rating: str
    :return: list
    """
    json_format = []
    rating_parameters = {
        "children": '"G"',
        "family": '"G", "PG", "PG-13"',
        "adult": '"R", "NC-17"'
    }
    if rating in rating_parameters.keys():
        query = f"""
                    SELECT title, rating, description
                    FROM netflix
                    WHERE rating in ({rating_parameters[rating]})
                """
        cursor.execute(query)
        movie_list = cursor.fetchall()
        for movie in movie_list:
            json_format.append({
                "title": movie[0],
                "rating": movie[1],
                "description": movie[2]
            }, )
        return json_format
    return "Введено не верное значение"


def choose_movie_by_genre(cursor, genre):
    json_format = []
    query = f"""
                SELECT title, description
                FROM netflix
                WHERE listed_in = '{genre}' AND type = 'Movie'
                ORDER BY release_year DESC
                LIMIT 10
            """
    cursor.execute(query)
    movie_list = cursor.fetchall()
    for movie in movie_list:
        json_format.append({
            "title": movie[0],
            "description": movie[1]
        }, )

    return json_format


def get_movie_cast_partners(cursor, actor_1, actor_2) -> list:
    """
    Функция, получает в качестве аргумента имена двух актеров, сохраняет всех актеров из колонки cast
    и возвращает список тех, кто играет с ними в паре больше 2 раз.
    :param cursor:
    :param actor_1: str
    :param actor_2: str
    :return: list
    """
    query = f"""
                SELECT `cast`
                FROM netflix
                WHERE `cast` like '%{actor_1}%' AND `cast` like '%{actor_2}%'
            """
    cursor.execute(query)
    movie_list = cursor.fetchall()
    actor_list = []
    for cast in movie_list:
        for actors in cast:
            actor_list.extend(actors.split(", "))
    counter = Counter(actor_list)
    result_list = []
    for actor, count in counter.items():
        if actor not in [actor_1, actor_2] and count > 2:
            result_list.append(actor)
    return result_list


def search_list_movie(cursor, type_movie, data, genre) -> list:
    """
    Функция, которая принимает тип картины (фильм или сериал), год выпуска и ее жанр и получает
    на выходе список названий картин с их описаниями в JSON.
    :param cursor:
    :param type_movie: str
    :param data: int
    :param genre: str
    :return: list
    """
    query = f"""
                    SELECT title, description
                    FROM netflix
                    WHERE type like '{type_movie}' AND release_year like {data} AND listed_in LIKE '{genre}'
                """
    cursor.execute(query)
    movie_list = cursor.fetchall()
    result_list = []
    for movie in movie_list:
        result_list.append({
            "title": movie[0],
            "description": movie[1]
        },)
    return result_list


print(get_movie_cast_partners(creat_connection(setting.DATABASE), "Jack Black", "Dustin Hoffman"))
print(search_list_movie(creat_connection(setting.DATABASE), "Movie", 2010, "Dramas"))
