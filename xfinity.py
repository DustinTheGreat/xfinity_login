from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import subprocess
import random
import string 


def random_email():
	domains = ["@gmail.com.com", "@hotmail.com", "@yahoo.com", "@msn.com"]
	name = "".join(random.choice(string.ascii_lowercase[:26]) for i in range(7))
	numbers = "".join(str(random.randint(1,10)) for x in range(4))
	
	USERNAME= name+numbers
	EMAIL = USERNAME + random.choice(domains)
	return(USERNAME, EMAIL)
def reset_wifi():
	subprocess.call(["sudo nmcli c del id xfinitywifi"], shell=True)
	subprocess.call(["sudo ifconfig wlp3s0 down"], shell=True)
	subprocess.call(["sudo macchanger -r wlp3s0"], shell=True)
	subprocess.call(["sudo ifconfig wlp3s0 up"], shell=True)
	time.sleep(15)
	subprocess.call(["nmcli d wifi connect xfinitywifi"], shell=True)



def signup():
	USERNAME, EMAIL = random_email()
	#setup
	chromedriver = 'chromedriver'
	driver = webdriver.Chrome()
	driver.get('http://10.232.0.1')
	#page1
	b = driver.find_element_by_id("amdocs_signup")
	b.click()

	#page2
	time.sleep(3)
	free = driver.find_element_by_id("offersFreeList1")
	free.click()
	c = driver.find_element_by_id("continueButton")
	c.click()
	n = driver.find_element_by_id("upgradeOfferCancelButton")
	n.click()

	#page 3 form
	driver.refresh()
	time.sleep(1)
	#pafe

	first =  driver.find_element_by_name("firstName")
	last = driver.find_element_by_name("lastName")
	username = driver.find_element_by_name("userName")
	email = driver.find_element_by_name("alternateEmail")
	question_option = driver.find_element_by_id("dk0-combobox")
	question1 = q1 = driver.find_element_by_id("dk0-What-was your first car (make and model)?")
	answer = driver.find_element_by_name("secretAnswer")
	password = driver.find_element_by_name("password")
	confirm_password = driver.find_element_by_name("passwordRetype")
	submit_button = driver.find_element_by_id("submitButton")

	#change to make unique
	first.send_keys("George")
	last.send_keys("Constanza")
	username.send_keys(USERNAME)
	email.send_keys(EMAIL)
	question_option.click()
	question1.click()
	answer.send_keys('answer')
	password.send_keys('randompass22')
	confirm_password.send_keys("randompass22")
	submit_button.click()
	#page4
	time.sleep(5)
	#wait to initialize need to chage to see when spinner stops
	activate_pass = driver.find_element_by_id("_orderConfirmationActivatePass")

#reset_wifi()
#time.sleep(3)
signup()
random_email()
