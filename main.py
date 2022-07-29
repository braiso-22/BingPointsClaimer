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
    i = 0
    while i < 39:
        try:
            browser.get("https://www.bing.com/search?q=" + str(i))
            i+=1
        except:
            continue


def dailyPromos():
    goToInnerContainer()
    allPromos = getPagePromos()

    print("Searches 1")
    try:
        for search in allPromos[0]:
            uiSearcher(browser, 40).until(
                EC.element_to_be_clickable(search)).click()
    except:
        print("No search promos avaliables")

    goToInnerContainer()

    uiSearcher(browser, 40).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "chevronUp"))).click()

    allPromos = getPagePromos()

    print("Searches 2")
    try:
        for search in allPromos[0]:
            uiSearcher(browser, 40).until(
                EC.element_to_be_clickable(search)).click()
    except:
        print("No search promos avaliables")


def getPagePromos():
    arrayOfPromos = list()
    arrayOfQuizes = list()
    arrayOfSearches = list()

    firstList = browser.find_elements(By.XPATH, "//div[@class='promo_cont']/a")
    for element in firstList:
        try:
            correctCircle = element.find_element(
                By.CLASS_NAME, "correctCircle")
        except:
            correctCircle = None

        if correctCircle:
            continue

        if "Test".lower() in element.find_element(By.XPATH, ".//p[@class='b_subtitle promo-title']").text.lower():
            arrayOfQuizes.append(element)
        else:
            arrayOfSearches.append(element)

    arrayOfPromos.append(arrayOfSearches)
    arrayOfPromos.append(arrayOfQuizes)

    return arrayOfPromos


def goToInnerContainer():
    callPromos()
    innerHtmlContainer = browser.find_element(By.ID, value="bepfm")
    browser.switch_to.frame(innerHtmlContainer)


def callPromos():
    goToBing()
    rewardsButton = uiSearcher(browser, 40).until(
        EC.element_to_be_clickable((By.ID, "id_rc")))
    time.sleep(1)
    rewardsButton.click()


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Microsoft user path not found as parameter')
        print('You can see it in edge://version/ as "Profile path"')
    else:
        main()
