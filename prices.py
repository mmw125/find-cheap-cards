from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

import winsound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second
winsound.Beep(frequency, duration)

driver = webdriver.Chrome()
url = "https://www.tcgplayer.com/product/{item}?Printing=Normal&page=1&Language=English&Condition=Lightly+Played|Near+Mint"
foil_url = "https://www.tcgplayer.com/product/{item}?Printing=Foil&page=1&Language=English&Condition=Lightly+Played|Near+Mint"

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

# {uuid: [non-foil, foil]}
# price_data = {}


@dataclass
class Card:
    uuid: str
    tcgplayerNormal: float | None
    tcgplayerFoil: float | None
    cardkingdomBuylistNormal: float | None
    cardkingdomBuylistFoil: float | None
    tcgplayerSku: int = None


cards: dict[str, Card] = {}

with open("AllPrices.json") as file:
    prices = json.load(file)
    date = prices['meta']['date']
    print("opened file")
    for uuid, item in prices["data"].items():
        if "paper" in item and "tcgplayer" in item["paper"]:
            cardKingdomBuylist = item["paper"].get("cardkingdom", {}).get("buylist", None)
            if cardKingdomBuylist and ("foil" in cardKingdomBuylist or "normal" in cardKingdomBuylist):
                buylistNormal = cardKingdomBuylist.get("normal", {}).get(date, None)
                buylistFoil = cardKingdomBuylist.get("foil", {}).get(date, None)
                if buylistFoil and buylistFoil > 10 or buylistNormal and buylistNormal > 10:
                    tcgplayer = item["paper"]["tcgplayer"]["retail"]
                    normal = tcgplayer.get("normal", {}).get(date, None)
                    foil = tcgplayer.get("foil", {}).get(date, None)
                    card = Card(uuid, tcgplayerNormal=normal, tcgplayerFoil=foil,
                                cardkingdomBuylistNormal=buylistNormal, cardkingdomBuylistFoil=buylistFoil)
                    print(card)

print("opening skus")
with open("TcgplayerSkus.json") as file:
    skus = json.load(file)
    print("opened file")
    for uuid, item in skus["data"].items():
        if uuid in cards:
            cards[uuid].tcgplayerSku = item[0]["productId"]

for card in cards:

