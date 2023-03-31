# from selenium import webdriver
from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.common.by import By
import pandas as pd
import time
import json

class WebScrape:
  def __init__(self, url,  next_page):
    self.url = url
    self.next_page = next_page

  def execute_scrape_shopee(self):
    url = self.url
    url_api = []
    has_next_age = self.next_page
    prefs = {"profile.managed_default_content_settings.images": 2}
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", prefs)
    options.add_argument("disable-infobars")
    # options.headless = True
    driver = webdriver.Chrome(options=options)

    datas = []
    try:
      if not has_next_age:
        driver.get(url)
        time.sleep(3)
      else:
        for num_page in range(0, 2):
          url_next_page = url + has_next_age + str(num_page)
          formatting_url_api = 'https://shopee.co.id/api/v4/search/search_items?by=relevancy&keyword=ssd&limit=60&newest={}&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2'.format(num_page * 60)
          url_api.append(formatting_url_api)
          driver.get(url_next_page)
          time.sleep(10)
          driver.set_page_load_timeout(1000)

      for request in driver.requests:
        if request.response:
          for api in url_api:
            if request.url.startswith(api):
              res = request.response
              #DECODE RESPONSE BODY
              body = decode(res.body, res.headers.get('Content-Encoding', 'Identity'))
              decode_to_utf8 = body.decode('utf8')
              datas_json = json.loads(decode_to_utf8)
              rows = datas_json['items']
              for i in range(0, len(rows)):
                get_data = rows[i]['item_basic']
                data_product = {
                  'Item ID'         : get_data['itemid'],
                  'Shop ID'         : get_data['shopid'],
                  'Name Product'    : get_data['name'],
                  'Brand'           : get_data['brand'],
                  'Rating Star'     : get_data['item_rating']['rating_star'],
                  'Price'           : int(get_data['price'] / 100000),
                  'Discount'        : get_data['discount'],
                  'Price Before Discount' : int(get_data['price_before_discount'] / 100000),
                  'Price Max'       : int(get_data['price_max'] / 100000),
                  'Price Max Before Discount' : int(get_data['price_max_before_discount'] / 100000),
                  'Price Min'       : int(get_data['price_min'] / 100000),
                  'Price Min Before Discount' : int(get_data['price_min_before_discount'] / 100000),
                  'Shop Location'   : get_data['shop_location'],
                  'Shop Verified'   : get_data['shopee_verified'],
                  'Stock'           : get_data['stock'],
                  'Name Variation'  : get_data['tier_variations'][0]['name'],
                  'Variation Option': get_data['tier_variations'][0]['options']
                }
                datas.append(data_product)
      driver.quit()
      return datas
    except Exception as e:
      err_mess = print("ERROR DURING SCRAPPING : ", e)
      return err_mess

  def convert_to_dataframe(self, data):
      data_frame = pd.DataFrame(data)
      return data_frame

  def convert_to_excel(self, filename, data):
      try:
        df = self.convert_to_dataframe(data)
        df.to_excel(filename)
        print(f"{filename} Success To Converted")
      except Exception as e:
        print(f"Failed To Convertion Data: {e}")



