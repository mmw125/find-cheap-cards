import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = "https://www.tcgplayer.com/product/{item}?Printing=Normal&page=1&Language=English&Condition=Lightly+Played|Near+Mint"
foil_url = "https://www.tcgplayer.com/product/{item}?Printing=Foil&page=1&Language=English&Condition=Lightly+Played|Near+Mint"

EXTRA_PRICE_INFO_CONTAINER_CLASS_NAME = "price-guide__points"
CURRENT_QUANTITY_CLASS_NAME = "price-points__lower__price"

AVG_DAILY_SOLD_CLASS_NAME = "sales-data__price"

driver = webdriver.Firefox()

def find_prices(card_id: int, foil: bool) -> [float, str]:
    fetch_url = foil_url.format(item=card_id) if foil else url.format(item=card_id)
    driver.get(fetch_url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "listing-item")))
    except selenium.common.exceptions.TimeoutException as e:
        return []

    try:
        extra_price_info_container = driver.find_element(By.CLASS_NAME, EXTRA_PRICE_INFO_CONTAINER_CLASS_NAME)
        current_quantity = extra_price_info_container.find_element(By.CLASS_NAME, CURRENT_QUANTITY_CLASS_NAME).text
        daily_sold = driver.find_element(By.CLASS_NAME, AVG_DAILY_SOLD_CLASS_NAME).text
        print(card_id, current_quantity, daily_sold)
    except selenium.common.exceptions.NoSuchElementException:
        pass



    for item in driver.find_elements(By.CLASS_NAME, "listing-item"):
            try:
                price = item.find_element(By.CLASS_NAME, "listing-item__listing-data__info__price").text.replace("$", "").replace(",", "")
                condition = item.find_element(By.CLASS_NAME, "listing-item__listing-data__info__condition").text
                return [float(price), condition]
            except selenium.common.exceptions.StaleElementReferenceException:
                continue
