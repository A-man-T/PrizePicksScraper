from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

############################################################################


# https://www.nba.com/stats/players/traditional?DateFrom=04/25/2023&DateTo=04/26/2023&PerMode=Totals&dir=A&sort=PTS scrape from here

PATH = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(PATH)

############################################################################

# Scraping PrizePicks
driver.get("https://app.prizepicks.com/")

# Waiting and closes popup
wait = WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "close")))
driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div/div/div[3]/button").click()
time.sleep(1)

# Creating tables for players
ppPlayers = []

# Now it will click NBA tab, change NBA to the sport of your liking supported by PrizePicks.
driver.find_element(By.XPATH, "//div[@class='name'][normalize-space()='MLB']").click()
time.sleep(2)

# Waits until stat container element is viewable
stat_container = WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "stat-container")))

# Finding all the stat elements within the stat-container such as Pass Yards, Receiving Yards, Receptions, etc.
categories = driver.find_element(By.CSS_SELECTOR, ".stat-container").text.split('\n')
time.sleep(2)

# Collecting categories
for category in categories:

    cat_string = "//div[@class='stat'][normalize-space()='{}']".format(category)

    driver.find_element(By.XPATH, "//div[text()='{}']".format(category)).click()

    projectionsPP = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".projection")))

    for projections in projectionsPP:
        names = projections.find_element(By.CLASS_NAME, "name").text
        pts = projections.find_element(By.CLASS_NAME, "presale-score").get_attribute('innerHTML')
        proptype = projections.find_element(By.CLASS_NAME, "text").get_attribute('innerHTML')
        date = projections.find_element(By.CLASS_NAME, "date").get_attribute('innerHTML')

        players = {
            'Name': names,
            'Points': pts,
            'Prop': proptype.replace("<wbr>", ""),
            'Date': date
        }
        ppPlayers.append(players)

dfProps = pd.DataFrame(ppPlayers)
#dfProps.to_csv('May24.csv')

print("These are all of the props offered by PP.", '\n')
print(dfProps)
print('\n')
