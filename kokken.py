import time, regex, binascii#, requests
from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
 
 
#def init_driver():
	#driver = webdriver.Firefox()
	#driver.wait = WebDriverWait(driver, 5)
	#return driver
 
 
#def download(driver, fullurl):
	#driver.get(fullurl)
	#try:
	#	box = driver.wait.until(EC.presence_of_element_located(
	#		(By.NAME, "q")))
	#	button = driver.wait.until(EC.element_to_be_clickable(
	#		(By.NAME, "btnK")))
	#	box.send_keys(query)
	#button.click()
	#except TimeoutException:
	#print("Box or Button not found in google.com")
 
 
#if __name__ == "__main__":
#driver = init_driver()
driver = webdriver.Firefox()
url = "http://base1.nijl.ac.jp/iview/Frame.jsp?DB_ID=G0003917KTM&C_CODE=XMI2-06402&IMG_SIZE=&PROC_TYPE=null&SHOMEI=【史記評林】&REQUEST_MARK=null&OWNER=null&IMG_NO="
cache = "about:cache-entry?storage=disk&context=&eid=&uri=http://image.nijl.ac.jp/cgi-bin/GetImage.cgi?file=XMI2/XMI2-06402/XMI2-06402-"
pages = 2295
find = r"(?<=\w{8}:\s\s)[\w\s]{64}" ###<---Find what?
#replace= r'N' ###<---Replace with what?
for p in range(1, pages + 1):
	if p % 100 == 0:
		driver.quit()
		driver = webdriver.Firefox()
	if p < 11: pstring = "000{0}".format(p-1)
	elif p < 101: pstring = "00{0}".format(p-1)
	elif p < 1001: pstring = "0{0}".format(p-1)
	else: pstring = str(p-1)
	fullurl = "{0}{1}".format(url, p)
	cacheurl = "{0}{1}.jpg".format(cache, pstring)
	#download(driver, fullurl)
	#r = requests.get(cacheurl)
	while True:
		try:
			driver.get(fullurl)
			time.sleep(5)
			driver.get(cacheurl)
			hexstring = driver.find_element_by_xpath("/html/body/pre").text
			hexarray = regex.findall(find, hexstring)
			hexdata = "".join(hexarray)
			hexdata = regex.sub(r"\s", r"", hexdata)
			with open("{0}.jpg".format(pstring), "wb") as f:
				f.write(binascii.unhexlify(hexdata))
				f.closed
			break
		except NoSuchElementException:
			print("Download error. Trying again...")
			time.sleep(10)

#print(hextext)
#time.sleep(5)
#driver.quit()