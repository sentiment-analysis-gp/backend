import requests
from bs4 import BeautifulSoup


def get_soup(url):
    r = requests.get('http://localhost:8050/render.html', params={'url': url})
    open("render.html", "w").write(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def get_reviews(soup, review_list):
    reviews = soup.find_all('div', {'data-hook': 'review'})
    try:
        for item in reviews:
            rating_element = item.find('i', {'data-hook': 'review-star-rating'})
            if rating_element is None:
                rating_element = item.find('i', {'data-hook': 'cmps-review-star-rating'})
            review = {
                'product': soup.title.text.replace('Amazon.co.uk:Customer reviews:', '').strip(),
                # 'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
                'rating': float(rating_element.text.replace('out of 5 stars', '').strip()),
                'body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
            }
            review_list.append(review)
    except:
        pass


def get_product_data(soup):
    title = soup.find('a', {'data-hook': 'product-link'}).text.strip()
    average_rating = soup.find('span', {'data-hook': 'rating-out-of-text'}).text
    total_ratings_and_reviews = soup.find('div', {'data-hook': 'cr-filter-info-review-rating-count'}).\
        find('span').text.strip()
    product_image = soup.find('img', {'data-hook': 'cr-product-image'})['src']

    histogram = {}
    for row in soup.find_all('tr', {'class': 'a-histogram-row'}):
        rating = row.find('td', {'class': 'aok-nowrap'}).find('a', {'class': 'a-link-normal'}).text.strip()
        percentage = row.find('td', {'class': 'a-text-right'}).find('a', {'class': 'a-link-normal'}).text.strip()
        histogram[rating] = percentage

    return {
        "title": title,
        "average_rating": average_rating,
        "total_ratings_and_reviews": total_ratings_and_reviews,
        "product_image": product_image,
        "histogram": histogram,
    }


def scrap():
    output_data = {}
    review_list = []
    for x in range(1, 999):
        soup = get_soup(
            f'https://www.amazon.com/AmazonBasics-Slot-Phone-Mount-Holder/product-reviews/B083KR68JW/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
        print(f'Getting page: {x}')
        if x == 1:
            output_data = get_product_data(soup)
        get_reviews(soup, review_list)
        print(len(review_list))
        if soup.find('li', {'class': 'a-disabled a-last'}):
            break

    output_data["reviews"] = review_list
    print('Fin.')
    return output_data
