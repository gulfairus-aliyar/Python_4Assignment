from bs4 import BeautifulSoup
import requests

BASE_URL = "https://coinmarketcap.com/currencies/"


def get_paragraphs(coin: str):
    r = requests.get(f"{BASE_URL}/{coin}")
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all(["p"])
    text = [result.text for result in results]
    return text
