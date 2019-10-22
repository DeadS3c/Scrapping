#!/usr/bin/python3

import requests
import sys
import time
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

indice = 0
proxyList = []
urlTestProxy = "http://icanhazip.com"

def getData(f):
	global indice
	global proxyList
	global urlTestProxy
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
		typ = "socks5"
		anon = "elite"
		country = "US"
		(proxies, statusProx) = getListProxy(typ, anon, country)
		if(statusProx == 200 and proxies):
			proxiesList = proxies.split('\n')
			for p in proxiesList:
				proxyList.append(typ.strip() + "://" + p.strip())
			proxy = setProxy()
			dataParse = parserData(url, f, proxy)
			for i in range(1,int(total_number)):
				print("---------> Pagina " + str(i) + " <-------------")
				urlParse = "https://www.locatefamily.com/Street-Lists/Spain/index-"+str(i)+".html"
				dataParse = parserData(urlParse, f, proxy)
				while(not dataParse):
					proxy = setProxy()
					dataParse = parserData(urlParse, f, proxy)

		else:
			print("[-] No proxies for party!")

def getListProxy(typ, anon, country):
    url = "https://www.proxy-list.download/api/v1/get?type="+typ
    if(anon):
        url += "&anon="+anon
    if(country):
        url += "&country="+country

    res = requests.get(url)
    return res.text, res.status_code

def setProxy():
	global indice
	global proxyList
	if(indice == len(proxyList) -1):
		indice = 0
	proxy = proxyList[indice]
	print(proxy)
	if(not testProxy(proxy)):
		indice = indice + 1
		setProxy()
	else:
		return proxy

def testProxy(proxy):
	global urlTestProxy
	proxies = dict(http=proxy,https=proxy)
	try:
		print("[+] Obtaining Proxy to play...")
		r = requests.get(urlTestProxy, proxies=proxies)
		print("\t[*]Response: " + r.text.strip())
		if(r.text.strip() == proxy.split("://")[1].split(":")[0]):
			print("[*] Proxy Correct! Lets Play!")
			return True
		else:
			print("[-] Proxy Error! Find Another one!")
			return False
	except Exception as e:
		print("Error: " + str(e))
		print("[-] Proxy Error! Find Another one!")
		return False
	return False

def parserData(url, f, proxy):
	proxies = dict(http=proxy, https=proxy)
	try:
		response = requests.get(url, proxies=proxies, verify=False, timeout=5)
	except Exception as e:
		print("Exception: " + str(e))
		return False
	if(response.status_code != 200):
		print("[-] Something goes wrong!")
		print("[-] Status Code: " + str(response.status_code))
		return False
	else:
		soup = BeautifulSoup(response.text, 'html.parser')
		cont = True
		i = 1
		while(i <= 60 and cont):
			try:
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
			except:
				i += 1
				pass
	return True

def main():
	f = open('crawlResults.txt', 'w+')
	getData(f)
	f.close()

if __name__ == '__main__':
	main()
