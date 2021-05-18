import sys

from flask import request, jsonify
import selectorlib
import requests
from dateutil import parser as dateparser

extractor = selectorlib.Extractor.from_yaml_file('selectors.yml')


def scrape(url):
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        "Accept-Encoding": "gzip, deflate",
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        "Connection": "close",
    }

    # Download the page using requests
    print("Downloading %s" % url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n" % url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d" % (url, r.status_code))
        return None
    # Pass the HTML of the page and create
    data = extractor.extract(r.text, base_url=url)
    open("downloaded.html", "w").write(r.text)
    if data["reviews"] is None:
        return {}
    reviews = []
    for r in data['reviews']:
        r["product"] = data["product_title"]
        r['url'] = url
        if r['rating'] is None:
            r['rating'] = r['rating2'].split(' out of')[0]
        else:
            r['rating'] = r['rating'].split(' out of')[0]
        date_posted = r['date'].split('on ')[-1]
        if r['images']:
            r['images'] = "\n".join(r['images'])
        r['date'] = dateparser.parse(date_posted).strftime('%d %b %Y')
        reviews.append(r)
    histogram = {}
    for h in data['histogram']:
        histogram[h['key']] = h['value']
    data['histogram'] = histogram
    data['average_rating'] = float(data['average_rating'].split('out')[0])
    data['reviews'] = reviews
    data['number_of_reviews'] = int(data['number_of_reviews'].split(" ")[0].replace(",", ""))
    return data


def scrap_data(url):
    split_url = url.split("/dp/")
    product_id = split_url[1].split("/")[0]
    reviews_url = split_url[0] + "/product-reviews/" + product_id + "/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8%26reviewerType=all_reviews"
    pages = []
    reviews = []
    output_data = {}
    while reviews_url is not None:
        data = scrape(reviews_url)
        pages.append(data)
        if data == {}:
            break
        output_data["average_rating"] = data["average_rating"]
        output_data["histogram"] = data["histogram"]
        output_data["number_of_reviews"] = data["number_of_reviews"]
        output_data["total_ratings_and_reviews"] = data["total_ratings_and_reviews"]
        output_data["product_image"] = data["product_image"]
        output_data["product_title"] = data["product_title"]
        reviews = reviews + data["reviews"]
        reviews_url = data["next_page"]

    output_data["reviews"] = reviews
    return jsonify(output_data)
