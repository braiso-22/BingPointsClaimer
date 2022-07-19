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

browser = webdriver.Edge(service=Service(
    "./driver/msedgedriver.exe"), options=browserOptions)

browser.get("https://bing.com/")

