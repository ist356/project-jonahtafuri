from playwright.sync_api import Playwright, sync_playwright
from time import sleep

def scraper(playwright: Playwright, category, price, time) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(f"https://www.eventbrite.com/d/ny--syracuse/{price}--{category}--events--{time}/?page=1")
    sleep(2)

    context.close()
    browser.close()
    # return df

if __name__ == "__main__":
    with sync_playwright() as p:
        scraper(p, "free", "this-weekend")