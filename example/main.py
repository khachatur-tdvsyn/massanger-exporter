import json
import time

from selenium import webdriver
from selenium.webdriver.common.webdriver import LocalWebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

ALL_DATA_FILE = 'all_data.json'
WHATSAPP_URL = 'https://web.whatsapp.com'

def login_qr(driver: LocalWebDriver):
    print('Opening WhatsApp')
    driver.get(WHATSAPP_URL)

    try:
        wait = WebDriverWait(driver, 90)
        element = wait.until(lambda driver: driver.find_element(By.CSS_SELECTOR, '._akaz'))
    except TimeoutException:
        print('No any QR for scanning. Quit.')
        return

    print('Screenshot of image. Quickly scan QR code in site')
    driver.get_screenshot_as_file('image.png')
    print('After 20 seconds opened another QR to scan again')
    time.sleep(20)
    print('Scan again')
    driver.get_screenshot_as_file('image.png')

    try:
        wait = WebDriverWait(driver, 120)
        element = wait.until(lambda driver: driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[3]/div/div[4]/header/header/div/div/h2/span/span/span/span"))
    except TimeoutException:
        print('Failed to login into whatsapp. Quit')
        return
    
    print('Obtaining necessary cookies and data in localStorage')
    driver_values = {
        'cookies': json.dumps(driver.get_cookies()),
        'sessions': driver.execute_script('return JSON.parse(JSON.stringify(localStorage))')
    }
    print('Saving all data in file')
    with open(ALL_DATA_FILE, 'w') as f:
        json.dump(driver_values, f)
        
    print('Closing remote webdriver')
    driver.close()

def enter(driver):
    print('Opening WhatsApp')
    driver.get(WHATSAPP_URL)

    try:
        wait = WebDriverWait(driver, 30)
        element = wait.until(lambda driver: driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[3]/div/div[4]/header/header/div/div/h2/span/span/span/span"))
    except TimeoutException:
        print('Failed to login into whatsapp. Quit')
        return

    print('Successfully logged in')

def login_local_storage(driver: LocalWebDriver):
    print('Reading last data')
    with open(ALL_DATA_FILE) as f:
        driver_data = json.load(f)
    
    driver_data['cookies'] 

    print('Opening WhatsApp')
    driver.get(WHATSAPP_URL)

    print('Setting up cookies')
    
    for c in driver_data['cookies']:
       driver.add_cookie(c)

    print('Setting up local storage')
    for k, v in driver_data['sessions'].items():
        script = f'localStorage.setItem("{k}",{json.dumps(v)})'
        print(script)
        driver.execute_script(script)
    
    print('Refreshing and waiting for logging in')
    driver.refresh()
    try:
        wait = WebDriverWait(driver, 30)
        element = wait.until(lambda driver: driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div/div[3]/div/div[4]/header/header/div/div/h2/span/span/span/span"))
    except TimeoutException:
        print('Failed to login into whatsapp. Quit')
        return

    print('Successfully logged in')


def main():
    print('Opening browser')

    # profile = webdriver.FirefoxProfile("/home/xac/snap/firefox/common/.mozilla/firefox/JMp3UtkV.Profile 1")
    
    options = webdriver.FirefoxOptions()

    # options.add_argument("--headless")
    options.add_argument("--profile")
    options.add_argument("/home/xac/workspace/projects/massanger_exporter/profiles/local_profile")
    #options.add_argument("/home/xac/snap/firefox/common/.mozilla/firefox/JMp3UtkV.Profile 1")
    # options.profile = webdriver.FirefoxProfile("/home/xac/snap/firefox/common/.mozilla/firefox/JMp3UtkV.Profile 1")
    # options.profile = webdriver.FirefoxProfile("/home/xac/workspace/projects/massanger_exporter/profiles/local_profile")

    geckodriver_path = "/snap/bin/geckodriver"  # specify the path to your geckodriver
    driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)

    driver = webdriver.Firefox(options=options, service=driver_service)
    # login_qr(driver)
    enter(driver)

if __name__ == '__main__':
    main()