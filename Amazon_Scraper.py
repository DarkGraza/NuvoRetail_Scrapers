from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date, datetime
import time
import re

sheets = pd.read_excel("C:/Users/chand/OneDrive/Desktop/Nuvoretail/Test_Problems/Problem1/AmazonInput.xlsx", sheet_name=['Code',"Location "])
code_df = sheets['Code']
locat_df = sheets['Location ']
data_list = []

for code in code_df['platform_code']:
    url = f"https://www.amazon.in/dp/{code}"
    print(url)
    for pin in locat_df['location']:
        driver = webdriver.Chrome()
        time.sleep(3)
        driver.get(url)
        time.sleep(5)
        data = {}
        pin = str(pin)
        print(pin)
        location_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@id="glow-ingress-block"]'))
            )
        location_button.click()
        time.sleep(3)

        location = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//input[@id="GLUXZipUpdateInput"]'))
            )
        location.send_keys(pin, Keys.ENTER)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, 'lxml')
        Present_date = date.today()
        not_available = soup.find(id="availability_feature_div").text.strip()
        print(not_available)
        if not_available.startswith("Currently"):
            price = location = status = delivery_days = delivery_fee = "Unavailable"
        else:
            print("product in stock")
            price = soup.find('span', class_="a-price-whole").text.split('.')
            price = price[0]
            status = "In Stock"

            del_container = soup.find(id="mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE")
            d = del_container.find_all('span')

            delivery_fee = d[0].get("data-csa-c-delivery-price")
            del_date = d[0].get("data-csa-c-delivery-time")


            tomorrow = del_date.split(',')
            tomorrow = tomorrow[0]

            print(tomorrow)
            if tomorrow == 'Tomorrow':
                days = 1
            else:
                # if the delivery month is Jan of the next year then this condition will sort it out
                date_object = datetime.strptime(del_date, "%A, %d %B")
                if date_object.month == 1 and Present_date.month != 1:
                    d_obj = date_object.replace(year=(datetime.today().year + 1))
                else:
                    d_obj = date_object.replace(year=datetime.today().year)
                days = (d_obj.date() - Present_date).days

            delivery_days =days

        try:
            units = soup.find(id="socialProofingAsinFaceout_feature_div").text.split()
            units = units[0]
        except Exception as e:
            print(f"Error : {e}")
            units = "Not Displayed"

        rating = soup.find('span', class_="reviewCountTextLinkedHistogram noUnderline").text.rsplit()
        location_text = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@id="glow-ingress-block"]'))
            ).text.split('\n')
        location = re.sub(r'[^\x20-\x7E]', '', location_text[1])
        data = {
            "Time_stamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Platform_Code": code,
            "Platform": "Amazon",
            "Selling_Price": price,
            "Rating": rating[0],
            "Status_Text": status,
            "Delivery_Days": delivery_days,
            "Location": location,
            "Product_URL": url,
            "Delivery_Fee": delivery_fee,
            "Unit_Sold": units,
        }
        print(data)
        data_list.append(data)
        driver.quit()

df2 = pd.DataFrame(data_list)
print(df2)
df2.to_excel("Amazon_Output.xlsx")