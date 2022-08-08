from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as uiSearcher
from selenium.webdriver.support import expected_conditions as EC

import random
import sys
import time

browserOptions = Options()

browser: webdriver.Edge


def main():

    initBrowser()

    initialPoints = getCurrentPoints()
    print(initialPoints)

    dailySearches()
    dailyPromos()

    earnedPoints = int(getCurrentPoints()) - int(initialPoints)
    print(f"Earned {earnedPoints}")
    print("Done")


def initBrowser():
    initOptions()
    global browser
    browser = webdriver.Edge(service=Service(
        "./driver/msedgedriver.exe"), options=browserOptions)
    goToBing()


def initOptions():
    # browserOptions.add_argument("start-maximized")
    userPath = "--user-data-dir=" + str(sys.argv[1])
    browserOptions.add_argument(userPath)

    browserOptions.add_argument('--profile-directory=Default')


def goToBing():
    inBing = False
    while not inBing:
        try:
            browser.get("https://bing.com/")
            inBing = True
        except:
            pass


def getCurrentPoints():
    goToBing()
    rewardsButton = uiSearcher(browser, 40).until(
        EC.element_to_be_clickable((By.ID, "id_rc")))
    return rewardsButton.get_attribute('innerHTML')


def dailySearches():
    i = 0
    while i < 39:
        try:
            browser.get("https://www.bing.com/search?q=" + str(i))
            i += 1
        except:
            continue


def dailyPromos():
    dailySearchPromos()
    dailyQuizPromos()


def dailySearchPromos():
    print("Searches 1")
    while True:
        goToInnerContainer()
        page1Searches = getPromosByType()
        if len(page1Searches) > 0:
            clickPromo(page1Searches[0])
        else:
            break
    pass

    print("Searches 2")
    while True:
        goToInnerContainer(dropdown=True)
        page2Searches = getPromosByType()
        if len(page2Searches) > 0:
            clickPromo(page2Searches[0])
        else:
            break
    pass


def dailyQuizPromos():
    goToInnerContainer()
    try:
        dailyTest = getPromosByType("test diario")[0]

        print("Quiz 1")
        executeDualAnswerQuiz(dailyTest)
    except:
        print("Can't run dailyTest")
    print("Quiz 2")
    while True:
        goToInnerContainer()
        page1Searches = getPromosByType("Test")
        if len(page1Searches) > 0:
            executeRegularQuiz(page1Searches[0])
        else:
            break
    pass
    while True:
        goToInnerContainer(dropdown=True)
        page1Searches = getPromosByType("Test")
        if len(page1Searches) > 0:
            executeRegularQuiz(page1Searches[0])
        else:
            break
    pass


def executeRegularQuiz(quiz):
    clickPromo(quiz)
    initButtonClickable = False
    while not initButtonClickable:
        try:
            uiSearcher(browser, 40).until(
                EC.element_to_be_clickable((By.ID, "rqStartQuiz"))).click()
            initButtonClickable = True
        except:
            pass

    while True:
        finishElement = browser.find_elements(By.ID, "quizCompleteContainer")

        if len(finishElement) > 0:
            break

        correctOptions = browser.find_elements(
            By.XPATH, '//div[@iscorrectoption="True"]')
        correctOptionsIds = list()
        for option in correctOptions:
            correctOptionsIds.append(option.get_attribute("id"))
        correctOptionsIds = list(filter(len, correctOptionsIds))
        i = 0
        while i < len(correctOptionsIds):
            try:
                uiSearcher(browser, 40).until(
                    EC.element_to_be_clickable((By.ID, correctOptionsIds[i]))).click()
                i += 1
                time.sleep(1)
            except:
                continue
        correctOptions = list()
    pass


def executeDualAnswerQuiz(quiz):
    clickPromo(quiz)

    randomNum = random.randint(0, 1)

    uiSearcher(browser, 40).until(
        EC.element_to_be_clickable((By.ID, ("btoption" + str(randomNum))))).click()

    goToBing()


def goToInnerContainer(dropdown=False):
    callPromos()

    innerHtmlContainer = browser.find_element(By.ID, value="bepfm")
    browser.switch_to.frame(innerHtmlContainer)

    if dropdown:
        clickDropdown()


def clickDropdown():
    uiSearcher(browser, 40).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "chevronUp"))).click()


def callPromos():
    goToBing()
    rewardsButton = uiSearcher(browser, 40).until(
        EC.element_to_be_clickable((By.ID, "id_rc")))
    time.sleep(1)
    rewardsButton.click()


def getPromosByType(type: str = "default"):
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

        if(type == "default"):
            type = "Test"
            if type.lower() not in element.accessible_name.lower():
                arrayOfSearches.append(element)
            type = "default"
        else:
            if type.lower() in element.accessible_name.lower():
                arrayOfSearches.append(element)
    return arrayOfSearches


def clickPromo(search):
    try:
        uiSearcher(browser, 40).until(
            EC.element_to_be_clickable(search)).click()
    except:
        print("No search avaliable")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Microsoft user path not found as parameter')
        print('You can see it in edge://version/ as "Profile path"')
    elif "\\YOUR-USER\\" in str(sys.argv[1]):
        print("You should replace \"YOUR-USER\" in the params with your username")
    else:
        main()
