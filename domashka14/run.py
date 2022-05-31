from flask import Flask, jsonify

import utils
import setting

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

@app.route("/movie/<title>")
def movie_by_name(title):
    return utils.search_movie_by_name(
        utils.creat_connection(setting.DATABASE), title)


@app.route("/movie/<int:year1>/to/<int:year2>")
def movie_by_range_year(year1, year2):
    return jsonify(utils.search_movie_by_range_year(
        utils.creat_connection(setting.DATABASE), year1, year2))


@app.route("/rating/<string:category>")
def movie_by_rating(category):
    return jsonify(utils.search_movie_by_rating(
        utils.creat_connection(setting.DATABASE), category))


@app.route("/genre/<string:genre>")
def movie_by_genre(genre):
    return jsonify(utils.choose_movie_by_genre(
        utils.creat_connection(setting.DATABASE), genre))


if __name__ == "__main__":
    app.run(debug=True, port=3030)