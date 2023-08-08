from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd 
import time



path ='/home/agustin/Escritorio/Data Scientist/Selenium/chromedriver_linux64/chromedriver'
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36")

driver = webdriver.Chrome(service=service, options=options)

def obtener_data_faltante(year):

    web = f'https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup'

    driver.get(web)

    print(f"Scraping data for year: {year}")


    matches = driver.find_elements(by='xpath', value='//*[@id="mw-content-text"]/div[1]/div[position() >= 17 and position() <= 64]/table/tbody/tr[1]')

    home = []
    score = []
    away = []


    for match in matches:
        home.append(match.find_element(by='xpath', value='./th[1]').text)
        score.append(match.find_element(by='xpath', value='./th[2]').text)
        away.append(match.find_element(by='xpath', value='./th[3]').text)

    dict_football = {'home': home, 'score': score, 'away': away}
    df_football = pd.DataFrame(dict_football)
    df_football['year'] = year
    time.sleep(2)
    return df_football

years = [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 
        1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 
        2010, 2014, 2018]

fifa = [obtener_data_faltante(year) for year in years]

driver.quit()

df_fifa = pd.concat(fifa, ignore_index=True)


df_fifa.to_csv('fifa_wordcup_missing_data.csv', index=False)