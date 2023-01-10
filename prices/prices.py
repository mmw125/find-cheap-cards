from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
url = "https://www.tcgplayer.com/product/{item}?Printing=Foil&page=1&utm_medium=card-detail-buy-foil&Language=English"
"""no-result"""


def find_prices(item: int):
    driver.get(url.format(item=item))

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "listing-item")))
    # title = driver.find_element(By.CLASS_NAME, "product-details__name").text
    # print(title)
    for item in driver.find_elements(By.CLASS_NAME, "listing-item"):
        price = item.find_element(By.CLASS_NAME, "listing-item__price").text
        condition = item.find_element(By.CLASS_NAME, "listing-item__condition").text
        # shipping_price = item.find_element(By.CLASS_NAME, "shipping-messages__price").text
        print(price, condition)


for i in range(212690, 212699):
    find_prices(i)
