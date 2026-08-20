from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv, dotenv_values
from time import sleep
from datetime import date, timedelta

class GloBirdScraper():
    def __init__(self):
        pass

    def getCSV(self):
        with sync_playwright() as self.playwright:
            browser = self.playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://myaccount.globirdenergy.com.au/wholesaledata")
            email, password = os.getenv("EMAIL"), os.getenv("PASSWORD")

            page.locator("#login_email").fill(email)
            page.locator("#login_password").fill(password)

            page.get_by_role("button", name="Sign in", exact=True).click()

            startdate = date.today() - timedelta(days=2)
            startdate = startdate.strftime("%d-%b-%Y")

            enddate = date.today() - timedelta(days=1)
            enddate = enddate.strftime("%d-%b-%Y")

            page.get_by_placeholder("Start date").click()
            page.get_by_placeholder("Start date").fill(startdate)
            page.get_by_placeholder("End date").click()
            page.get_by_placeholder("End date").fill(enddate)
            page.keyboard.press("Enter")

            svg = page.locator('svg[role="img"][data-icon="download"]').filter(
            has=page.locator('title:text("download meter read summary")')
            )

            with page.expect_download() as dl_info:
                svg.click()
            download = dl_info.value
            download.save_as(f"summary-{date.today()}.csv")

            browser.close()

def main():
    load_dotenv()
    scraper = GloBirdScraper()
    scraper.getCSV()

main()