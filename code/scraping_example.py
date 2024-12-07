import re
from playwright.sync_api import Playwright, sync_playwright
from time import sleep
# import menuitemextractor as mie
from menuitem import MenuItem
import pandas as pd

def tullyscraper(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.tullysgoodtimes.com/menus/")
    sleep(2)
    listings_selector = page.query_selector("div.foodmenu__content")
    sections = listings_selector.query_selector_all("div.foodmenu__menu-section")
    scraped_data = []
    for section in sections:
        items = section.query_selector_all("div.foodmenu__menu-item-wrapper")
        # print(items)
        # TODO Write code here
        for item in items:
            item_category = section.get_attribute("id")
            item_name = item.query_selector("p.foodmenu__menu-item__name")
            item_price = item.query_selector("span.foodmenu__menu-item__price")
            item_desc = item.query_selector("p.foodmenu__menu-item__desc")

            item_name = item_name.inner_text() if item_name else "N/A"
            item_price = item_price.inner_text() if item_price else "N/A"
            item_desc = item_desc.inner_text() if item_desc else "N/A"
            clean_price = float(item_price.replace('$',''))

            # new_entry = mie.extract_menu_item(item_category, item_price, item_name, item_desc)
            menu_item = MenuItem(name = item_name, 
                    price = clean_price, 
                    category= item_category, 
                    description=item_desc)
            scraped_data.append(menu_item.to_dict())
    df = pd.DataFrame(scraped_data)
    df.to_csv("cache/tullys_menu.csv", index=False)    


        # ---------------------

    context.close()
    browser.close()
    return df