import time
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pywebcopy import save_website
from pywebcopy import WebPage
import pywebcopy
from bs4 import BeautifulSoup
import pandas as pd
pywebcopy.config['bypass_robots'] = True
from datetime import datetime
from os import path

if __name__ == "__main__":

	print(os.getcwd())
	# params
	league_id = 2098926112
	today = datetime.today().strftime('%Y-%m-%d')
	dataset_name = today + ".csv"
	url = 'https://fantasy.espn.com/basketball/league/standings?leagueId=%s' %league_id
	
	if path.exists(today + ".csv"):

		print("today's standings have already been scraped.")

	else:

		# open chrome browser
		from webdriver_manager.chrome import ChromeDriverManager
		driver = webdriver.Chrome(ChromeDriverManager().install())
		driver.get(url);
		time.sleep(5)
		print('Opening league page')

		# # accept cookies
		driver.implicitly_wait(8)
		try:
			driver.find_element_by_xpath("//button[contains(@id, 'accept-btn')]").click()
		except:
			print('Cookies not supported!')
		else:
			print('Accepting cookies')


		## collect tables
		time.sleep(5)
		page = driver.page_source
		soup = BeautifulSoup(page, 'html.parser')
		tables = soup.find_all("table")
		print('Collecting relevant tables')

		# scrape data
		# standings table is actually 3 separate tables. 
		# table 3 contains rank and team names, and table 4 contains the data
		# I scrape each table separately then join together. 
		time.sleep(5)
		table = tables[4]
		tab_data = [[cell.text for cell in row.find_all(["th","td"])]
		                        for row in table.find_all("tr")][2:]

		headers = [[cell.text for cell in row.find_all(["th","td"])]
		                        for row in table.find_all("tr")][1]
		df_data = pd.DataFrame(tab_data, columns = headers)

		# scrape team names & ranks
		table = tables[3]
		tab_rownames = [[cell.text for cell in row.find_all(["th","td"])]
		                        for row in table.find_all("tr")][2:]
		df_names = pd.DataFrame(tab_rownames, columns = ['Rk', 'Team'])

		# scrape games played
		table = tables[5]
		tab_data = [[cell.text for cell in row.find_all(["th","td"])]
		                        for row in table.find_all("tr")][2:]

		headers = [[cell.text for cell in row.find_all(["th","td"])]
		                        for row in table.find_all("tr")][1]

		df_gp = pd.DataFrame(tab_data, columns = headers)

		# build dataframe
		df = df_names.join(df_data)
		df = df.join(df_gp)
		print(df)
		
		# add date column
		df['date'] = today

		# export to csv
		df.to_csv(dataset_name, index = False)
		
		# close browser
		driver.quit()
		print('Quitting browser')

		print("Dataset has been successfully exported to 'data' as ", dataset_name)

