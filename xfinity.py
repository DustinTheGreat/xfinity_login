#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
import sys
import os



def random_email():
	domains = ["@gmail.com.com", "@hotmail.com", "@yahoo.com", "@msn.com"]
	name = "".join(random.choice(string.ascii_lowercase[:26]) for i in range(7))
	numbers = "".join(str(random.randint(1,10)) for x in range(4))
	
	USERNAME= name+numbers
	EMAIL = USERNAME + random.choice(domains)
	return(USERNAME, EMAIL)


def change_mac(pbar):
	subprocess.call(["sudo nmcli c del id xfinitywifi"], stderr=open(os.devnull, 'wb'), stdout=open(os.devnull, 'wb'), shell=True)
	subprocess.call(["sudo ifconfig wlp3s0 down"], shell=True)
	time.sleep(1)
	try:
		subprocess.call(["sudo macchanger -r wlp3s0"], stderr=open(os.devnull, 'wb'), stdout=open(os.devnull, 'wb'), shell=True)
	except OSError:
		time.sleep(3)
		try:
			subprocess.call(["sudo macchanger -r wlp3s0"],stderr=open(os.devnull, 'wb'), stdout=open(os.devnull, 'wb'), shell=True)
		except OSError:
			subprocess.call(["sudo service network-manager restart"], shell=True)
			time.sleep(10)
			main()
	
	pbar.update(5)

def connect_wifi(pbar):
	wifi_up = subprocess.call(["sudo ifconfig wlp3s0 up"], stderr=open(os.devnull, 'wb'), shell=True)
	if wifi_up != 0:
		#troubleshooting network issues
		#try unblocking wifi card and if that does work restart wifi service
		subprocess.call(["sudo rfkill unblock wifi; sudo rfkill unblock all"], shell=True)
		time.sleep(2)
		wifi_up = subprocess.call(["sudo ifconfig wlp3s0 up"],stderr=open(os.devnull, 'wb'), shell=True)
		if wifi_up != 0:
			subprocess.call(["sudo service network-manager restart"], shell=True)
			print("-----restarting------")
			time.sleep(10)
			#subprocess.call("sudo systemctl start networking")
			#time.sleep(5)
			main()
		else:
			pbar.update(10)

	else:
		pbar.update(10)

	connect = subprocess.call(["nmcli d wifi connect xfinitywifi"], stderr=open(os.devnull, 'wb'),stdout=open(os.devnull, 'wb'), shell=True)
	if connect !=0:
		time.sleep(5)
		connect = subprocess.call(["nmcli d wifi connect xfinitywifi"], stderr=open(os.devnull, 'wb'),stdout=open(os.devnull, 'wb'), shell=True)
		if connect !=0:
			subprocess.call(["sudo service network-manager restart"], shell=True)
			print("     Can't connect to WiFi")
			print("-----restarting------")
			time.sleep(10)
			#subprocess.call(["sudo systemctl start networking"])
			#time.sleep(5)
			main()
		else:
			pbar.update(20)
	else:
		pbar.update(20)


def setup(pbar):
	capa = DesiredCapabilities.CHROME
	capa["pageLoadStrategy"] = "none"
	options = Options()
	options.add_argument('--headless')
	driver = webdriver.Chrome(executable_path="./chromedriver", desired_capabilities=capa,options=options)
	
	driver.implicitly_wait(60)
	driver.get('http://10.232.0.1')
	pbar.update(10)
	return(driver)


def signup(pbar):

	USERNAME, EMAIL = random_email()
	driver = setup(pbar)

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
	#page 3 
	capa = DesiredCapabilities.CHROME
	capa["pageLoadStrategy"] = "none"


	#wait.until(EC.presence_of_element_located((By.ID, '#dk0-combobox')))
	pbar.update(20)
	time.sleep(3)
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
	pbar.update(20)

	driver.implicitly_wait(60)
	activate_pass = driver.find_element_by_id("_orderConfirmationActivatePass")
	activate_pass.click()
	pbar.update(20)

def main():
	pbar = tqdm(total=100) 
	change_mac(pbar)
	time.sleep(2)
	connect_wifi(pbar)
	time.sleep(1)
	signup(pbar)
	pbar.close()
	print("You got internet bitch!")


main()