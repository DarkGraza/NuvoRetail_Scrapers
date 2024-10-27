import requests
from bs4 import BeautifulSoup

import json
import pandas as pd
from datetime import datetime


sheets = pd.read_excel(r"C:\Users\chand\OneDrive\Desktop\Nuvoretail\Test_Problems\Problem3\input.xlsx", sheet_name=['urls', "location"])
urls_df = sheets['urls']
locat_df = sheets['location']
urls_df = urls_df.drop_duplicates()
locat_df = locat_df.drop_duplicates()
print(urls_df)
data_list = []

for u in urls_df['url']:
    print(u)
    r = requests.get(u)
    soup = BeautifulSoup(r.content, 'lxml')
    scr = soup.find("script", type='application/ld+json')
    json_data = json.loads(scr.text)
    image_url = json_data['image']
    skus = image_url.split('/')
    sku = skus[8]
    prod_name = json_data['name']
    data = {}
    for pin in locat_df['location']:
        payload = {}
        headers = {
            'sec-ch-ua-platform': '"Windows"',
            'Referer': 'https://www.purplle.com/product/meera-anti-dandruff-shampoo-with-small-onion-and-fenugreek-650ml',
            'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            'is_SSR': 'false',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXZpY2VfaWQiOiJic09KNmNDQW9LWWY0YVYzWDYiLCJtb2RlX2RldmljZSI6ImRlc2t0b3AiLCJtb2RlX2RldmljZV90eXBlIjoid2ViIiwiaWF0IjoxNzI5OTM3OTIyLCJleHAiOjE3Mzc3MTM5MjIsImF1ZCI6IndlYiIsImlzcyI6InRva2VubWljcm9zZXJ2aWNlIn0.NWfMdXJ3LXwHFP8wlJ8l_P89XV3Nhxv4YfrQRzmCidA',
            'visitorppl': 'bsOJ6cCAoKYf4aV3X6',
            'mode_device': 'desktop'
        }


        pincode_api = f"https://www.purplle.com/neo/cart/pincode-check?pincode={pin}&productid={sku}"
        price_api = f"https://www.purplle.com/neo/catalog/retrieveprice?productId={sku}&pincode={pin}"
        review_api = f"https://www.purplle.com/neo/catalog/reviews?productId={sku}&page=1&sortBy=mh"

        r_pin = requests.get(pincode_api, headers=headers, data=payload)
        r_price = requests.get(price_api)
        r_review = requests.get(review_api)

        pincode = json.loads(r_pin.text)
        price = json.loads(r_price.text)
        review = json.loads(r_review.text)

        print(pincode)
#price object data
        status = price['item']['availability']['stockStatus']
        status_text = lambda status: "In Stock" if bool(status) else "Out of Stock"
        status_check = status_text(status)
        mrp = price['item']['availability']['mrp']
        sp = price['item']['availability']['offerPrice']
        discount = price['item']['availability']['discount']

#review object data
        rating = review['reviewStats']['avgRating']
        no_of_rating = review['reviewStats']['countRating']
        no_of_review = review['reviewStats']['countReviews']

#pincode object data
        delivery = lambda pincode: pincode['delivery_by'] if bool(pincode['status']) else pincode['message']
        del_text = delivery(pincode)

        today = datetime.now()
        present = today.strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "time_stamp": present,
            "Platform": "purple",
            "platform_code": sku,
            "Location": pin,
            "Pname": prod_name,
            "status_text": status_check,
            "Sp": sp,
            "Offer in %": discount,
            "Mrp": mrp,
            "Rating": rating,
            "no_of_rating": no_of_rating,
            "no_of_review": no_of_review,
            "prod_url": u,
            "delivery_days": del_text,
            }
        data_list.append(data)

df = pd.DataFrame(data_list)
print(data_list)
df.to_excel('Purple_Output.xlsx')