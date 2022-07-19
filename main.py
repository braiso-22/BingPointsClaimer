from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WebUi
from selenium.webdriver.support import expected_conditions as EC


import time
import pyautogui

browserOptions = Options()
browserOptions.add_argument("start-maximized")
# TODO change to your path
browserOptions.add_argument("--user-data-dir= ??????")
browserOptions.add_argument('--profile-directory=Default')

browser = webdriver.Edge(service=Service(
    "./driver/msedgedriver.exe"), options=browserOptions)

browser.get("https://bing.com/")

cookiesAcceptButton = WebUi(browser, 20).until(
    EC.element_to_be_clickable((By.ID, "bnp_btn_accept")))

cookiesAcceptButton.click()