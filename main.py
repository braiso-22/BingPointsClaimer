from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as uiSearcher
from selenium.webdriver.support import expected_conditions as EC

import sys
import time

browserOptions = Options()

browser: webdriver.Edge


def main():
    initOptions()
    initBrowser()
    dailySearches()
    dailyPromos()

    print("Done")


def initOptions():
    # browserOptions.add_argument("start-maximized")

    userPath = "--user-data-dir=" + str(sys.argv[1])
    browserOptions.add_argument(userPath)

    browserOptions.add_argument('--profile-directory=Default')


def initBrowser():
    global browser
    browser = webdriver.Edge(service=Service(
        "./driver/msedgedriver.exe"), options=browserOptions)
    goToBing()


def goToBing():
    browser.get("https://bing.com/")


def dailySearches():
    for i in range(0, 39):
        browser.get("https://www.bing.com/search?q=" + str(i))


def dailyPromos():
    goToBing()
    allQuizes = getAllPromos()
    for quiz in allQuizes:
        print(quiz)





def getAllPromos():
    callPromos()
    arrayOfQuizes = list()
    innerHtmlContainer = browser.find_element(By.ID, value="bepfm")

    browser.switch_to.frame(innerHtmlContainer)

    firstList = browser.find_elements(By.XPATH, "//div[@class='promo_cont']/a")
    for link in firstList:
        arrayOfQuizes.append(link.get_attribute("href"))

    uiSearcher(browser, 40).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "chevronUp"))).click()

    secondList = browser.find_elements(
        By.XPATH, "//div[@class='promo_cont']/a")
    for link in secondList:
        arrayOfQuizes.append(link.get_attribute("href"))

    return arrayOfQuizes


def callPromos():
    rewardsButton = uiSearcher(browser, 40).until(
        EC.element_to_be_clickable((By.ID, "id_rc")))
    time.sleep(1)
    rewardsButton.click()


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Microsoft user path not found')
        print('You can see it in edge://version/ as "Profile path"')
    else:
        main()
