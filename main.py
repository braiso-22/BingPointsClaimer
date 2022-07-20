from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WebUi
from selenium.webdriver.support import expected_conditions as EC

browserOptions = Options()

browser: webdriver.Edge


def main():
    initOptions()
    initBrowser()
    dailySearches()

    print("Done")


def initOptions():
    browserOptions.add_argument("start-maximized")
    # TODO change to your path
    browserOptions.add_argument("--user-data-dir=??????")
    browserOptions.add_argument('--profile-directory=Default')


def initBrowser():
    global browser
    browser = webdriver.Edge(service=Service(
        "./driver/msedgedriver.exe"), options=browserOptions)
    browser.get("https://bing.com/")


def dailySearches():
    for i in range(0, 34):
        browser.get("https://www.bing.com/search?q="+str(i))


if __name__ == "__main__":
    main()
