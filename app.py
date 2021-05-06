from flask import Flask, request

from scraper import scrap_data

app = Flask(__name__)


@app.route('/')
def hello_world():
    url = request.headers.get("product-url")
    pages = scrap_data(url)
    return pages


if __name__ == '__main__':
    app.run()
