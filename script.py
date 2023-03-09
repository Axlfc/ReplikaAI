import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Replace with your own Firefox profile path
firefox_profile_path = 'C:\\Users\\AxelFC\\AppData\\Local\\Mozilla\\Firefox\\Profiles\\oktmx2r7.default-release'

# Create a FirefoxOptions object with your profile path
firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('--profile')
firefox_options.add_argument(firefox_profile_path)

# Create a new Firefox driver with your options
driver = webdriver.Firefox(options=firefox_options)

# Load the Replika web app
driver.get('https://my.replika.com/')

# Wait for the page to load
time.sleep(5)

while True:
    # Find the chat input box and send a message
    input_box = driver.find_element(By.CSS_SELECTOR, 'textarea.TextArea-sc-10kop8p-0')
    message = input('You: ')
    input_box.send_keys(message + Keys.RETURN)

    time.sleep(8)
    # Wait for the bot to respond
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[aria-live="polite"]')))
    all_responses = driver.find_elements(By.CSS_SELECTOR, 'span[aria-live="off"]')
    bot_responses = driver.find_elements(By.CSS_SELECTOR, 'span[aria-live="polite"]')

    # Print the bot's response(s)
    # print("exclude my own message: " + message)
    # From my own message to the last span[aria-live="off"]
    # print("B: " + bot_responses[-1].text)
    
    bot_text_responses = []
    for xd in all_responses:
        bot_text_responses.append(xd.text)
    
    index = bot_text_responses.index(message)
    print("INDEX: " + str(index))
    # bot_responses = bot_responses[index:]
    print(len(bot_responses))
    '''all_responses = all_responses[index:]
    for response in all_responses:
        if response.text == "":
            pass
        else:
            print('B:', response.text)'''
    
    for response in bot_responses:
        if response.text == "":
            pass
        else:
            print('B:', response.text)

# Quit the driver
driver.quit()