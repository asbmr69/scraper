from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def get_trending_topics():
    # Initialize the WebDriver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    # Open Twitter Explore page
    driver.get('https://twitter.com/explore/tabs/trending')
    time.sleep(5)  # Allow time for the page to load

    trends = []
    for i in range(3, 13):
        try:
            xpath = f'//div[@aria-label="Timeline: Explore"]/div/div[{i}]/div/div/div/div/div[2]/span/span'
            element = driver.find_element(By.XPATH, xpath)
            trends.append(element.text)
        except Exception as e:
            print(f"Error finding element {i}: {e}")

    driver.quit()
    return trends

if __name__ == "__main__":
    trends = get_trending_topics()
    for i, trend in enumerate(trends, 1):
        print(f"Trend {i}: {trend}")