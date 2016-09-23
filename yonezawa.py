#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests,time#,os

def main():
	waittime = 10 #must be set to at least 30 or files won't download
	print("Please enter the URL of the book you wish to download:")
	while True:
		book_url = input("") #get URL of book
		if book_url[:43] == "http://www.library.yonezawa.yamagata.jp/dg/": break
		else: print("Invalid input! Be sure to enter the full URL including http://.")
	book_id = book_url.split("/")[-1][:-5] #get book id
	print("Book ID: "+book_id)
	images_url = "http://www.library.yonezawa.yamagata.jp/dg/data/"+book_id+"/"
	soup = BeautifulSoup(requests.get(images_url).text) #soup of images URL
	url_array = []
	for vol in soup.find_all('a', href=True):
		if vol["href"] != "/dg/data/":
			url_array.append(vol['href'])
	counter = 0
	for i in url_array:
		counter = counter + 1
		if counter > 1:
			vol_url = images_url+i
			vol_soup = BeautifulSoup(requests.get(vol_url).text)
			for pic in vol_soup.find_all('a', href=True):
				if pic["href"] != "/dg/data/"+book_id+"/":
					print("Now downloading "+vol_url+pic["href"])
					r = requests.get(vol_url+pic["href"])
					with open(pic["href"], "wb") as f:
						f.write(r.content)
						f.closed
						time.sleep(waittime)

if __name__ == "__main__":
	main()
