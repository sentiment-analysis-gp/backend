import requests
from langdetect import detect

from constants import rapid_api_key


def get_product_info(product_id):
    url = "https://amazon-product-reviews-keywords.p.rapidapi.com/product/details"
    querystring = {"asin": product_id}
    headers = {
        'x-rapidapi-key': rapid_api_key,
        'x-rapidapi-host': "amazon-product-reviews-keywords.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    json = response.json()
    product_data = json["product"]
    return {
        "title": product_data["title"],
        "images": product_data["images"],
        "mainImage": product_data["main_image"],
        "price": product_data["price"],
        "rating": product_data["reviews"]["rating"],
        "totalReviews": product_data["reviews"]["total_reviews"],
    }


def get_product_reviews(product_id):
    url = "https://amazon-product-reviews-keywords.p.rapidapi.com/product/reviews"
    reviews = []
    querystring = {"asin": product_id, "page": "1", "country": "US", "variants": "1", "top": "0"}
    headers = {
        'x-rapidapi-key': rapid_api_key,
        'x-rapidapi-host': "amazon-product-reviews-keywords.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    json = response.json()
    if "reviews" in json:
        new_page_reviews = json["reviews"]
        for review in new_page_reviews:
            if detect(review['review']) != "en":
                continue
            else:
                reviews.append(review)
        return reviews
    return {
        "reviews": []
    }
