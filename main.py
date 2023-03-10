from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import os
import configparser

config = configparser.RawConfigParser()
config.read(os.path.join(os.getcwd(), 'config.ini'))

user_data = os.path.join(os.getcwd(), 'UserProfile')
options = Options()
options.add_argument(f'user-data-dir={user_data}')

# chat_url = 'https://discord.com/channels/849331368558198803/1077509383400984636'
login_url = config['Urls']['login_url']
root_url = config['Urls']['root_url']
chat_url = config['Urls']['chat_url']
text = config['Text']['text']
input_selector = config['Selectors']['input_selector']

work_time_in_minutes = int(config['Time']['work_time_in_minutes'])
message_repeat_time_in_seconds = int(config['Time']['message_repeat_time_in_seconds'])

while True:
    what_to_do = input('Write "login" to login, or "start" to start: ')

    if what_to_do.lower() == 'login':
        first_url = login_url

        break
    elif what_to_do.lower() == 'start':
        first_url = root_url

        break
    else:
        print(f'"{what_to_do}"', ' is not valid value\n')

driver = webdriver.Chrome('chromedriver', options=options)

try:
    driver.get(first_url)

    if first_url == login_url:
        _ = input("Press enter when you are logged in >>")

    driver.get(chat_url)

    _ = input('Press enter when chat is loaded >>')
    print('Here we go!')

    end_time = time.time() + work_time_in_minutes * 60

    while time.time() < end_time:
        chat = driver.find_element(By.CSS_SELECTOR, input_selector)

        ActionChains(driver).click(chat).perform()

        time.sleep(1)

        ActionChains(driver).send_keys(text).perform()
        time.sleep(0.5)

        if text[0] == '/':
            ActionChains(driver).send_keys(Keys.ENTER, Keys.ENTER).perform()
        else:
            ActionChains(driver).send_keys(Keys.ENTER).perform()

        time.sleep(message_repeat_time_in_seconds)
finally:
    print('Bot stopped!')
    driver.quit()

