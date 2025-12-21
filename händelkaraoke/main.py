from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
import subprocess

def wait_till(element):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, element))
    )

def click(element):
    element(By.XPATH, element).click()

def search(term):
    element(By.XPATH, searchbar).send_keys(Keys.CONTROL + "a" , Keys.BACKSPACE)
    element(By.XPATH, searchbar).send_keys(term, "karaoke" + Keys.ENTER)

options = Options()
duration =  "//div[@class='ytp-left-controls']//span[@class='ytp-time-duration']"
firefox_profile = FirefoxProfile()
options.profile = "/home/milo/.mozilla/firefox/jsycqlvk.Karaoke/"

driver = webdriver.Firefox( options=options)
element = driver.find_element

searchbar = "//input[@placeholder='Search']"
first_vid = "//body/ytd-app/div[@id='content']/ytd-page-manager[@id='page-manager']/ytd-search[@role='main']/div[@id='container']/ytd-two-column-search-results-renderer[@class='style-scope ytd-search']/div[@id='primary']/ytd-section-list-renderer[@class='style-scope ytd-two-column-search-results-renderer']/div[@id='contents']/ytd-item-section-renderer[@class='style-scope ytd-section-list-renderer']/div[@id='contents']/ytd-video-renderer[1]/div[1]/ytd-thumbnail[1]/a[1]"
driver,get("https://google.com")
sleep(3)
driver.get("https://youtube.com")
wait_till(searchbar)
search("fka twigs")
time = wait_till(duration)
print(time.text)


#Spotify pausieren und anmachen accordinglyyyy
subprocess.run(["playerctl",  "-p", "spotify", "play-pause"])
