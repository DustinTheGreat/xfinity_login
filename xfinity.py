#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import subprocess
import random
import string 
from tqdm import tqdm




def random_email():
	domains = ["@gmail.com.com", "@hotmail.com", "@yahoo.com", "@msn.com"]
	name = "".join(random.choice(string.ascii_lowercase[:26]) for i in range(7))
	numbers = "".join(str(random.randint(1,10)) for x in range(4))
	
	USERNAME= name+numbers
	EMAIL = USERNAME + random.choice(domains)
	return(USERNAME, EMAIL)


def reset_wifi():
	subprocess.call(["sudo nmcli c del id xfinitywifi", stdout=DEVNULL], shell=True)
	subprocess.call(["sudo ifconfig wlp3s0 down",], shell=True)
	time.sleep(1)
	try:
		subprocess.call(["sudo macchanger -r wlp3s0", stdout=DEVNULL], shell=True)
	except:
		time.sleep(5)
		subprocess.call(["sudo macchanger -r wlp3s0"], stdout=DEVNULL, shell=True)

	time.sleep(2)
	try:
		subprocess.call(["sudo ifconfig wlp3s0 up"], shell=True)
	except:
		subprocess.call(["sudo rfkill unblock wifi; sudo rfkill unblock all"], shell=True)
		time.sleep(1)
	time.sleep(5)
	subprocess.call(["nmcli d wifi connect xfinitywifi"], shell=True)
	



def signup():
	USERNAME, EMAIL = random_email()
	#setup
	capa = DesiredCapabilities.CHROME
	capa["pageLoadStrategy"] = "none"
	options = Options()
	options.add_argument('--headless')
	chromedriver = 'chromedriver'
	driver = webdriver.Chrome(desired_capabilities=capa, options=options)
	time.sleep(10)
	driver.get('http://10.232.0.1')
	#page1
	driver.implicitly_wait(60)
	b = driver.find_element_by_id("amdocs_signup")
	b.click()

	#page2

	driver.implicitly_wait(60)
	free = driver.find_element_by_id("offersFreeList1")
	free.click()
	c = driver.find_element_by_id("continueButton")
	c.click()
	driver.implicitly_wait(60)
	n = driver.find_element_by_id("upgradeOfferCancelButton")
	n.click()
	#page 3 form
	#page
	capa = DesiredCapabilities.CHROME
	capa["pageLoadStrategy"] = "none"


	#wait.until(EC.presence_of_element_located((By.ID, '#dk0-combobox')))
	time.sleep(5)
	driver.execute_script("window.stop();")
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
	#wait to initialize need to chage to see when spinner stops
	#wait.until(EC.presence_of_element_located((By.ID, '_orderConfirmationActivatePass')))

	driver.implicitly_wait(60)
	activate_pass = driver.find_element_by_id("_orderConfirmationActivatePass")
	activate_pass.click()
	print("You got internet bitch!")



reset_wifi()
signup()

