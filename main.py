import time
import json
from datetime import datetime
from webbrowser import BackgroundBrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchWindowException
from pymongo import MongoClient
import requests
from selenium import *
from flask import Flask, render_template, jsonify
import threading


# Configure your ProxyMesh credentials
#PROXYMESH_URL = "http://amazing:Tushartiwari21@us-ca.proxymesh.com:31280:31280"

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['twitter_trends']
collection = db['trending_topics']

def get_driver():
    options = webdriver.ChromeOptions()
    #options.add_argument(f'--proxy-server={PROXYMESH_URL}')
    options.headless = False
    driver = webdriver.Chrome(options=options)
    return driver

def login_to_twitter(driver, username, password):
    driver.get("https://twitter.com/login")
    time.sleep(5)

    # Use WebDriverWait to wait until the elements are present
    wait = WebDriverWait(driver, 20)
    
    # Updated locators
    
    username_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@autocomplete='username']")))
    
    username_input.send_keys(username)
    username_input.send_keys(Keys.RETURN)
    
    time.sleep(5)  # wait for the password field to appear
    
    
    password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@autocomplete='current-password']")))
    
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)

def click_explore_button(driver):
     # Handling potential pop-ups
    try:
        not_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Not now']"))
        )
        not_now_button.click()
    except TimeoutException:
        pass  # Continue if the pop-up does not appear

    # Find and click the "Explore" button
    try:
        # Wait for the "Explore" button to be present
        explore_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[2]" )))
        
        explore_button.click()
        time.sleep(5)
    except TimeoutException:
        print("Explore button not found.")


def get_trending_topics(driver):
     
    time.sleep(10)
  
    
    trends = []
    xpaths = [
        '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/section/div/div/div[3]/div/div/div/div/div[2]',
        '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/section/div/div/div[4]/div/div/div/div/div[2]',
        '//*[@id="id__34dotb6j6sz"]/div[2]',
        '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/section/div/div/div[6]/div/div/div/div/div[2]',
        '/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/section/div/div/div[7]/div/div/div/div/div[2]']

    for xpath in xpaths:
        try:
           element = driver.find_element(By.XPATH, xpath)
           trends.append(element.text)
        except NoSuchElementException as e:
           print(f"Error finding element for XPath {xpath}: {e}")

    return trends

def save_to_mongodb(trends, ip):
    unique_id = str(datetime.now().timestamp())
    data = {
        "_id": unique_id,
        "trend1": trends[0] if trends else None,
        "trend2": trends[1] if len(trends) > 1 else None,
        "trend3": trends[2] if len(trends) > 2 else None,
        "trend4": trends[3] if len(trends) > 3 else None,
        "trend5": trends[4] if len(trends) > 4 else None,
        "datetime": datetime.now(),
        "ip_address": ip
    }
    collection.insert_one(data)
    return data


def main(username, password):
    driver = get_driver()
    try:
        login_to_twitter(driver, username, password)
        click_explore_button(driver)

        trends = get_trending_topics(driver)
        ip = requests.get('https://api.ipify.org').text
        result = save_to_mongodb(trends, ip)
    finally:
        driver.quit()
    return result





app = Flask(__name__,template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-script')
def run_script():
    TWITTER_USERNAME = "testers545245"
    TWITTER_PASSWORD = "*******"
    result = main(TWITTER_USERNAME, TWITTER_PASSWORD)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
