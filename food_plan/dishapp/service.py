import requests
from bs4 import BeautifulSoup
from func_timeout import func_set_timeout


# парсинг цены ингредиента с перекрестка)
@func_set_timeout(20)
def get_price(ingredient_title: str) -> float:
    try:
        main_url = "https://www.perekrestok.ru/cat/search?search="
        search_str = ingredient_title.strip()
        search_str = search_str.replace(" ", "%20")
        page = requests.get(f"{main_url}{search_str}")
        soup = BeautifulSoup(page.text, "html.parser")
        not_found = soup.find_all("div", {"class": "notify-title"})
        prices = soup.find_all("div", {"class": "price-new"})
        try:
            price = prices[0].text.replace(" ₽", "")
        except:
            return -1

        if not_found:
            return -1
        else:
            try:
                return float(price.replace(',', '.'))
            except:
                return -1
    except:
        return -1









