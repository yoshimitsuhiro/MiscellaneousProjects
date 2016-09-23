import time, requests#, regex, binascii
from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

def main():
	driver = webdriver.Firefox()
	url = "http://pds.lib.harvard.edu/pds/view/15755632"
	bookid = url.split("/")[-1]
	firstpage = 2245
	pages = 3687
	driver.get("{0}?n={1}".format(url, firstpage))
	time.sleep(5)
	maximizeimage(driver)
	for p in range(firstpage, pages + 1):
		getpage(driver, bookid, p)

def maximizeimage(driver):
	driver.switch_to.frame(driver.find_element_by_name("citation")) #Switch to navigation frame
	maxbutton = driver.find_element_by_xpath("//*[@id='maximum']") #Find maximize button
	maxbutton.click() #Maximize image
	time.sleep(5)
	driver.switch_to.default_content() #Go back to parent frame

def getpage(driver, bookid, p):
	driver.switch_to.frame(driver.find_element_by_name("content")) #Switch to content frame
	img = driver.find_element_by_xpath("//img[contains(@title,'Sequence {0} of')]".format(p)) #Find image element
	src = img.get_attribute("src") #find image source
	r = requests.get(src) #Download image
	#Determine filename
	if p < 10: filename = "000{0}.jpg".format(p)
	elif p < 100: filename = "00{0}.jpg".format(p)
	elif p < 1000: filename = "0{0}.jpg".format(p)
	else: filename = "{0}.jpg".format(p)
	#Write file
	with open(filename, "wb") as f:
		f.write(r.content)
		f.closed
	driver.switch_to.default_content() #Go back to parent frame
	driver.switch_to.frame(driver.find_element_by_name("citation")) #Switch to navigation frame
	nextbutton = driver.find_element_by_xpath("//a[contains(@href,'/pds/view/{0}?n={1}')]".format(bookid, p + 1)) #Find next page button
	nextbutton.click() #Go to next page
	time.sleep(5)

if __name__ == "__main__":
	main()