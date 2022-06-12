#Qianyun Shen 



import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
def scrapeOne():
	data = []
	driver = webdriver.Chrome()
	driver.get('https://www.livesudoku.com/en/sudoku/medium/')
	
	soup = BeautifulSoup(driver.page_source,'lxml')
	whole = soup.find('div',id = 'playarea').find_all('tr')
	for i in whole:
		cell = i.find_all('td',class_='cellnormal')
		for j in cell:
			if j.span:
				data.append(j.span.string)
			else:
				data.append('')
	
	print(data)
	
data = []
def scrapeAll():
	global data
	data1 = []
	driver = webdriver.Chrome()
	driver.get('https://www.livesudoku.com/en/sudoku/easy/')
	
	soup = BeautifulSoup(driver.page_source,'lxml')
	whole = soup.find('div',id = 'playarea').find_all('tr')
	for i in whole:
		cell = i.find_all('td',class_='cellnormal')
		for j in cell:
			if j.span:
				data1.append(j.span.string)
			else:
				data1.append('')
	data.append(data1)
	num = 1
	while num < 100:
		data1 = []
		driver.find_element_by_xpath('//*[@id="buttonsarea"]/table[2]/tbody/tr[3]/td').click()
		driver.find_element_by_xpath('//*[@id="newsudokuwindow"]/table/tbody/tr[1]/td[1]').click()
		soup = BeautifulSoup(driver.page_source,'lxml')
		whole = soup.find('div',id = 'playarea').find_all('tr')
		for i in whole:
			cell = i.find_all('td',class_='cellnormal')
			for j in cell:
				if j.span:
					data1.append(j.span.string)
				else:
					data1.append('')
		data.append(data1)
		num += 1
	with  open ('sudoku1.csv','w') as f:
		writer = csv.writer(f,delimiter=',')
		writer.writerows(data)



	

