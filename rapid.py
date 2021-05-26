import requests
from langdetect import detect


def get_product_info(product_id):
    url = "https://amazon-product-reviews-keywords.p.rapidapi.com/product/details"
    querystring = {"asin": product_id}
    headers = {
        'x-rapidapi-key': "",
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
    page = "1"
    reviews = []
    while page is not None:
        querystring = {"asin": product_id, "page": f"{page}", "country": "US", "variants": "1", "top": "0"}
        headers = {
            'x-rapidapi-key': "53f349a00fmsh359482cbd05ebacp18fb42jsn6d0295b88309",
            'x-rapidapi-host': "amazon-product-reviews-keywords.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        json = response.json()
        new_page_reviews = json["reviews"]
        if len(new_page_reviews) == 0:
            break
        for review in new_page_reviews:
            if detect(review) != "en":
                continue
            else:
                reviews = reviews.append(review)
        page = json["next_page"]
    return reviews

