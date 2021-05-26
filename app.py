from flask import Flask, request, jsonify

from predictor import predict_reviews
from rapid import get_product_info, get_product_reviews

app = Flask(__name__)


@app.route('/info')
def get_info():
    url = request.headers.get("product-url")
    product_id = get_product_id(url)
    product_info = get_product_info(product_id)
    return jsonify(product_info)


@app.route('/reviews')
def get_reviews():
    url = request.headers.get("product-url")
    product_id = get_product_id(url)
    product_reviews = get_product_reviews(product_id)
    prediction = predict_reviews(product_reviews)
    return jsonify(prediction)


def get_product_id(product_url):
    split = product_url.split("/dp/")
    product_id = split[1].split("/")[0]
    return product_id


if __name__ == '__main__':
    app.run()
