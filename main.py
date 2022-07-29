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
    dailySearches()
    dailyPromos()

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
    browser.get("https://bing.com/")


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
    goToInnerContainer()
    page1Searches = getPagePromos()[0]

    print("Searches 1")
    clickPromos(page1Searches)

    goToInnerContainer(dropdown=True)

    page2Searches = getPagePromos()[0]

    print("Searches 2")
    clickPromos(page2Searches)


def dailyQuizPromos():
    goToInnerContainer()
    page1Quizes = getPagePromos()[1]

    print("Quizes 1")
    executeDualAnswerQuiz(page1Quizes[0])

    pass


def executeRegularQuiz(quiz):
    clickPromos(list(quiz))

    uiSearcher(browser, 40).until(
        EC.element_to_be_clickable((By.ID, "rqStartQuiz"))).click()

    # TODO While id="quizCompleteContainer" is Not present

    # TODO Find isCorrectOption=true and add to list the ids

    # TODO Click by id from the list and remove it from list

    # TODO When list is empty fill it again


def executeDualAnswerQuiz(quiz):
    quizList = list()
    quizList.append(quiz)
    clickPromos(quizList)

    randomNum = random.randint(0, 1)

    uiSearcher(browser, 40).until(
        EC.element_to_be_clickable((By.ID, ("btoption" + str(randomNum))))).click()

    goToBing()


def goToInnerContainer(dropdown=False):
    if dropdown:
        clickDropdown()

    callPromos()
    innerHtmlContainer = browser.find_element(By.ID, value="bepfm")
    browser.switch_to.frame(innerHtmlContainer)


def clickDropdown():
    uiSearcher(browser, 40).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "chevronUp"))).click()


def callPromos():
    goToBing()
    rewardsButton = uiSearcher(browser, 40).until(
        EC.element_to_be_clickable((By.ID, "id_rc")))
    time.sleep(1)
    rewardsButton.click()


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


def clickPromos(searches):
    try:
        for search in searches:
            uiSearcher(browser, 40).until(
                EC.element_to_be_clickable(search)).click()
    except:
        print("No search promos avaliables")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Microsoft user path not found as parameter')
        print('You can see it in edge://version/ as "Profile path"')
    elif "\\YOUR-USER\\" in str(sys.argv[1]):
        print("You should replace \"YOUR-USER\" in the params with your username")
    else:
        main()
