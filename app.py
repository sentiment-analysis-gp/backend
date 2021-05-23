from flask import Flask, request, jsonify

from predictor import predict_reviews
from scraper import scrap_data
from soup_scraper import scrap

app = Flask(__name__)


@app.route('/')
def hello_world():
    url = request.headers.get("product-url")
    pages = scrap_data(url)
    return pages


@app.route('/soup')
def soup_scraper():
    output_data = scrap()
    prediction = predict_reviews(output_data["reviews"])
    output_data["prediction"] = prediction
    return jsonify(output_data)


if __name__ == '__main__':
    app.run()
