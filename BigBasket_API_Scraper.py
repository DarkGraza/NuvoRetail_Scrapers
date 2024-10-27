import requests
import json
from datetime import datetime
import pandas as pd

slugs = ['kelloggs', 'chips']
data_list = []
for slug in slugs:
  page = 0
  rank = 1
  while (page<2):
    page += 1
    url = f"https://www.bigbasket.com/listing-svc/v2/products?type=ps&slug={slug}&page={page}"

    payload = {}
    headers = {
      'accept': '*/*',
      'accept-language': 'en-US,en;q=0.9',
      'content-type': 'application/json',
      'cookie': 'x-entry-context-id=100; x-entry-context=bb-b2c; _bb_locSrc=default; x-channel=web; _bb_loid=j:null; _bb_bhid=; _bb_nhid=1723; _bb_vid=NDMwOTYwNTcwMzM2ODMwNDQ2; _bb_dsevid=; _bb_dsid=; _bb_cid=1; csrftoken=TdwHz09qwtBybGwJgyH5OY5rGqzMzWEg7CT80fTLAQvL3tgopbrTG7g3xEMVYfG9; _bb_home_cache=27dcc695.1.visitor; _bb_bb2.0=1; is_global=1; _bb_addressinfo=; _bb_pin_code=; _bb_sa_ids=10654; _is_tobacco_enabled=0; _is_bb1.0_supported=0; _bb_cda_sa_info=djIuY2RhX3NhLjEwMC4xMDY1NA==; is_integrated_sa=0; bb2_enabled=true; bigbasket.com=3884d0b9-3cd5-481e-888f-2cf82d79f8c5; ufi=1; jarvis-id=fd2d0fc6-1af7-4d50-bf2e-44c8538c8140; _gcl_aw=GCL.1729754455.Cj0KCQjw4Oe4BhCcARIsADQ0csnfD6pNM64vG6NdOzXgHqAdkmP4srkGfcKGE9TBTozRmQrVLGro4sUaAo-ZEALw_wcB; _gcl_gs=2.1.k1^$i1729754451^$u160754478; _gcl_au=1.1.1719173725.1729754455; adb=0; _gid=GA1.2.1480671948.1729754455; _gac_UA-27455376-1=1.1729754455.Cj0KCQjw4Oe4BhCcARIsADQ0csnfD6pNM64vG6NdOzXgHqAdkmP4srkGfcKGE9TBTozRmQrVLGro4sUaAo-ZEALw_wcB; _fbp=fb.1.1729754454974.518309331742663722; _bb_tc=0; _bb_aid="MzA4NTgxODk5Nw=="; _bb_rdt="MzEwNDk4Nzc5MA==.0"; _bb_rd=6; _ga=GA1.1.171513351.1729754455; ts=2024-10-25%2015:05:48.277; csurftoken=3ODi0g.NDMwOTYwNTcwMzM2ODMwNDQ2.1729923765005.m6PAIMkVDsedWDtNqVfDmW5bZXUeKHC9aXeP0UPw448=; _ga_FRRYG5VKHX=GS1.1.1729923800.12.0.1729923800.60.0.0; csurftoken=3ODi0g.NDMwOTYwNTcwMzM2ODMwNDQ2.1729923765005.m6PAIMkVDsedWDtNqVfDmW5bZXUeKHC9aXeP0UPw448=',
      'priority': 'u=1, i',
      'referer': 'https://www.bigbasket.com/ps/?q=kelloggs',
      'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
      'x-channel': 'BB-WEB',
      'x-tracker': 'd0bdde01-3c77-4f15-a086-5ee9326883a7'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    json_data = json.loads(response.text)
    products = json_data['tabs'][0]['product_info']['products']
    present = datetime.now()

    for product in products:
      data = {}
      timestamp = present.strftime("%Y-%m-%d %H:%M:%S")
      p_id = product['id']
      brand = product['brand']['name']
      prod_name = product['desc']
      weight = product['w']
      main = "https://www.bigbasket.com"
      prod_url = main + product['absolute_url']
      sp = product['pricing']['discount']['prim_price']['sp']
      mrp = product['pricing']['discount']['mrp']
      rating = product['rating_info']['avg_rating']
      no_of_rating = product['rating_info']['rating_count']
      no_of_review = product['rating_info']['review_count']
      platform = "BigBasket"
      try:
        sponsored = product['additional_attr']['info'][2]['label']
      except:
        sponsored = "Not"

      if product['pricing']['offer'] == {} or product['pricing']['offer']['offer_entry_text'] == '':
        offer = "Unavailable"
      else:
        offer = product['pricing']['offer']['offer_entry_text']

      data = {
        "time_stamp": timestamp,
        "keyword": slug,
        "brand": brand,
        "pname": prod_name,
        "platform": "BigBasket",
        "platform_code": p_id,
        "sp": sp,
        "mrp": mrp,
        "rating": rating,
        "no_of_rating": no_of_rating,
        "no_of_review": no_of_review,
        "rank": rank,
        "prod_url": prod_url,
        "sponsored": sponsored,
        "weight": weight,
        "offer": offer
      }
      data_list.append(data)
      rank += 1

df = pd.DataFrame(data_list)
df.to_excel('BigBasket_Output.xlsx')



