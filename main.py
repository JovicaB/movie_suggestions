from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.search_title import MovieSearcher
from backend.suggestions import ClearAndMergeResults
from backend.modal import TitleInfo


application = Flask(__name__)
app = application
CORS(app)


@app.route("/search_title", methods=["POST"])
def search_title():
    input_data = request.get_json()
    titles_list = MovieSearcher(input_data).sort()

    return jsonify(titles_list)


@app.route("/title_suggestions", methods=["POST"])
def title_suggestions():
    input_data = request.get_json()
    titles_list = []
    titles_list = ClearAndMergeResults(input_data).merge_results()

    return jsonify(titles_list)


@app.route("/imdb_data", methods=["POST"])
def imdb_data():
    input_data = request.get_json()
    modal_data = TitleInfo(input_data).modal_data()

    return jsonify(modal_data)


if __name__ == '__main__':
    app.run(host='localhost',  port=5000,  debug=True)
