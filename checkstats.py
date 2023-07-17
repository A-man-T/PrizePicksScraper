from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd


start = "05/09/2023"
end = "05/10/2023"
csvName = "test"
#Parse the CSV File

df = pd.read_csv(csvName+'.csv')

print(df)

if 'Outcome' not in df:
    df['Outcome'] = 0
    




####################################
PATH = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(PATH)


website = "https://www.nba.com/stats/players/traditional?DateFrom=" #04/25/2023&DateTo=04/26/2023


dates = start +"&DateTo=" + end

website = website + dates

driver.get(website)
time.sleep(10)

webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

#driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[2]/div/button").click()
time.sleep(2)
driver.find_element(By.CLASS_NAME, "CromFiltersAdd_button__WNMWN").click()
#driver.find_element(By.CSS_SELECTOR, "CromFiltersAdd_button__WNMWN").click()







for index,rows in df.iterrows():
    driver.find_element(By.CLASS_NAME, "CromFiltersInput_ddVal__ZGVeO").clear()
    driver.find_element(By.CLASS_NAME, "CromFiltersInput_ddVal__ZGVeO").send_keys(rows.Name)
    time.sleep(1)
    stats = driver.find_element(By.CLASS_NAME, "Crom_body__UYOcU").text.split('\n')
    parsed_stats = stats[0].split() 
    print(stats)
    print(parsed_stats)
    
    value = -1 
    if rows.Prop == 'Points':
        value = parsed_stats[9]
    elif rows.Prop == 'Rebounds':
        value = parsed_stats[21]
    elif rows.Prop == 'Assists':
        value = parsed_stats[22] 

    print(value)
    print(rows.Points)
    print(type(value))
    print(type(rows.Points))
    if(float(value)>rows.Points):
        print(69696969)
        df.at[index, 'Outcome'] = 1

print(df)
df.to_csv(csvName+'Outcomes.csv')





