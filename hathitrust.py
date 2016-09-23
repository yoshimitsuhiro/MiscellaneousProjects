#from PyPDF2 import PdfFileMerger, PdfFileReader
from bs4 import BeautifulSoup
import requests, time, os


book_id = "uc1.$xxxxxxx" #"mdp.xxxxxxxxxxxxxx"
#print(book_id)
page = 44 #first page
lastpage = 98
waittime = 5
#waitlimit = 16
#waitcount = 0
while page <= lastpage:
	if page < 10:
		filename = "000{0}.pdf".format(page)
	elif page < 100:
		filename = "00{0}.pdf".format(page)
	else:
		filename = "0{0}.pdf".format(page)
	print("Now downloading page {0} of {1}.".format(page, lastpage))
	payload = {"id": book_id, "orient": 0, "size": 100, "seq": page, "attachment": 0}
	while True:
		r = requests.get("http://babel.hathitrust.org/cgi/imgsrv/download/pdf", params=payload)
		soup = BeautifulSoup((r).text)
		#print(soup.prettify())
		#print(soup.title.text)
		if soup.title: #.text == "Hathi Trust Digital Library - Resource Unavailable":
			time.sleep(30)
			r = requests.get("http://babel.hathitrust.org/cgi/imgsrv/download/pdf", params=payload)
		else: break
	with open(filename, "wb") as f:
		f.write(r.content)
		f.closed
	page += 1
	time.sleep(waittime)
	#waitcount +=1
	#if waitcount == waitlimit:
	#	time.sleep(waittime)
	#	waitcount = 0

'''
fullfilename = "book.pdf"
merger = PdfFileMerger()
for f in filenames:
	merger.append(PdfFileReader(open(f, "rb")))
merger.write(fullfilename)
for d in filenames:
	os.remove(d)
'''