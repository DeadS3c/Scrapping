#!/usr/bin/python3

import requests
import sys
import time
from bs4 import BeautifulSoup

def getData(f):
	url = "https://www.locatefamily.com/Street-Lists/Spain/index.html"
	response = requests.get(url)
	if(response.status_code != 200):
		print("[-] Something goes wrong!")
		print("[-] Status Code: " + str(response.status_code))
		exit(0)
	else:
		soup = BeautifulSoup(response.text, 'html.parser')
		pag = soup.find("ul", {"class":"pagination"})
		numbers = pag.find_all("a")
		total_number = numbers[len(numbers) - 1].get('href').split('-')[2].split('.')[0]
		parserData(url, f)
		for i in range(1,int(total_number)):
			urlParse = "https://www.locatefamily.com/Street-Lists/Spain/index-"+str(i)+".html"
			parserData(urlParse, f)
			time.sleep(3)

def parserData(url, f):
	response = requests.get(url)
	if(response.status_code != 200):
		print("[-] Something goes wrong!")
		print("[-] Status Code: " + str(response.status_code))
		exit(0)
	else:
		soup = BeautifulSoup(response.text, 'html.parser')
		cont = True
		i = 1
		while(i <= 60 and cont):
			cell = soup.find(id=i)
			if(soup.find(id=i+1)):
				cont = True
			else:
				cont = False
			rows = cell.find_all('li')
			address = ""
			telephone = ""
			name = ""
			surname = ""
			for row in rows:
				if(row.find("span", {"itemprop":"streetAddress"})):
					address = row.find("span", {"itemprop":"streetAddress"}).string
				elif(row.find("a", {"class":"phone-link"})):
					telephone = row.find("a", {"class":"phone-link"}).get('href')
				else:
					if(row.find("span", {"itemprop":"givenName"})):
						name = row.find("span", {"itemprop":"givenName"}).string
					if(row.find("span", {"itemprop":"familyName"})):
						surname = row.find("span", {"itemprop":"familyName"}).string
			print("****** Item " + str(i) + " ******")
			print("[+]Name: " + str(name).strip() + " " + str(surname).strip())
			print("[+]Telephone: " + str(telephone).strip())
			print("[+]Address: " + str(address).strip() + "\n")
			f.write("******* Item " + str(i) + " ********\n")
			f.write("Name: " + str(name).strip() + " " + str(surname).strip() + "\n")
			f.write("Telephone: " + str(telephone).strip() + "\n")
			f.write("Address: " + str(address).strip() + "\n\n")
			i += 1

def main():
	f = open('crawlResults.txt', 'w+')
	getData(f)
	f.close()

if __name__ == '__main__':
	main()
