from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# import winsound
# frequency = 2500  # Set Frequency To 2500 Hertz
# duration = 1000  # Set Duration To 1000 ms == 1 second
# winsound.Beep(frequency, duration)

driver = webdriver.Chrome()
url = "https://www.tcgplayer.com/product/{item}?Printing=Normal&page=1&Language=English&Condition=Lightly+Played|Near+Mint"
foil_url = "https://www.tcgplayer.com/product/{item}?Printing=Foil&page=1&Language=English&Condition=Lightly+Played|Near+Mint"


@dataclass
class Card:
    uuid: str
    tcgplayer_normal: float | None
    tcgplayer_foil: float | None
    cardkingdom_buylist_normal: float | None
    cardkingdom_buylist_foil: float | None
    tcgplayer_sku: int = None


def find_prices(id: int, foil: bool):
    fetch_url = foil_url.format(item=id) if foil else url.format(item=id)
    print(fetch_url)
    driver.get(fetch_url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "listing-item")))
    try:
        title = driver.find_element(By.CLASS_NAME, "product-details__name").text
    except Exception as e:
        pass
    for item in driver.find_elements(By.CLASS_NAME, "listing-item"):
        price = item.find_element(By.CLASS_NAME, "listing-item__price").text.replace("$", "").replace(",", "")
        condition = item.find_element(By.CLASS_NAME, "listing-item__condition").text
        return [title, float(price), condition]
   def find_cheap_cards():
    cards: dict[str, Card] = {}

    with open("AllPrices.json") as file:
        prices = json.load(file)
        date = prices['meta']['date']
        print("opened file")
        for uuid, item in prices["data"].items():
            if "paper" in item and "tcgplayer" in item["paper"]:
                cardkingdom_buylist = item["paper"].get("cardkingdom", {}).get("buylist", None)
                if cardkingdom_buylist and ("foil" in cardkingdom_buylist or "normal" in cardkingdom_buylist):
                    buylist_normal = cardkingdom_buylist.get("normal", {}).get(date, None)
                    buylist_foil = cardkingdom_buylist.get("foil", {}).get(date, None)
                    if (buylist_foil and buylist_foil > 10) or (buylist_normal and buylist_normal > 10):
                        tcgplayer = item["paper"]["tcgplayer"].get("retail", {})
                        normal = tcgplayer.get("normal", {}).get(date, None)
                        foil = tcgplayer.get("foil", {}).get(date, None)
                        card = Card(uuid, tcgplayer_normal=normal, tcgplayer_foil=foil,
                                    cardkingdom_buylist_normal=buylist_normal, cardkingdom_buylist_foil=buylist_foil)
                        cards[uuid] = card

    print("opening skus")
    with open("TcgplayerSkus.json") as file:
        skus = json.load(file)
        for uuid, item in skus["data"].items():
            if uuid in cards:
                cards[uuid].tcgplayer_sku = item[0]["productId"]

    for card in cards.values():
        if card.cardkingdom_buylist_foil and card.cardkingdom_buylist_foil > 10:
            title, price, condition = find_prices(card.tcgplayer_sku, True)
            if price < card.cardkingdom_buylist_foil:
                print(title, price, condition)

        if card.cardkingdom_buylist_normal and card.cardkingdom_buylist_normal > 10:
            title, price, condition = find_prices(card.tcgplayer_sku, False)
            if price < card.cardkingdom_buylist_normal:
                print(title, price, condition)
        time.sleep(card.tcgplayer_sku % 20)


find_cheap_cards()
