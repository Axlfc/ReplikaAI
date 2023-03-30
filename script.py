import os
import sys
import time
import colorama
from selenium.common import NoSuchElementException

import process_system
from dotenv import load_dotenv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service


load_dotenv()
# os.environ['MOZ_HEADLESS'] = '1'

if process_system.plat() == "Windows":
    firefox_profile_path = os.path.expanduser("~") + os.sep + 'AppData' + os.sep + 'Local' + os.sep + 'Mozilla' + os.sep + 'Firefox' + os.sep + 'Profiles' + os.sep + 'inmersprofile.default-release'
else:
    firefox_profile_path = os.path.expanduser("~") + "/snap/firefox/common/.mozilla/firefox/inmersprofile.default-release"

# Create a FirefoxOptions object with your profile path
firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('--profile')
firefox_options.add_argument(firefox_profile_path)

# service = Service(log_path=os.devnull)

# Create a new Firefox driver with your options
try:
    # driver = webdriver.Firefox(options=firefox_options, service=service)
    driver = webdriver.Firefox(options=firefox_options)
except:
    print("ERROR")
    driver.quit()

email = os.environ["REPLIKA_CLIENT_EMAIL"]
password = os.environ["REPLIKA_CLIENT_PASSWORD"]
# Navigate to the Replika login page
driver.get("https://my.replika.com/")

# login_button = driver.find_elements_by_xpath("//a[@href='/login' and text()='Log in']")
try:
    login_button = driver.find_element(By.XPATH, '//a[contains(text(), "Log in")]')

    if login_button:
        # Click on the login button to navigate to the login page
        login_button.click()

        # Wait for the email input box to appear
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'login-email'))
        )

        # Enter your email address
        email_input.send_keys(email)

        # Wait for the password input box to appear
        password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-password')))

        # Enter your password
        password_input.send_keys(password)

        # Submit the login form
        password_input.submit()

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.url_contains('https://my.replika.com/'))
except:
    # No login button found.
    pass

# Wait for the page to load
time.sleep(5)


def replika(message):
    initial_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
    try:
        # Find the chat input box and send a message
        input_box = driver.find_element(By.CSS_SELECTOR, 'textarea.TextArea-sc-10kop8p-0')
        add_message(message, initial_time)
        if message == "exit" or message == "quit":
            driver.quit()
            exit(0)

        input_box.send_keys(message + Keys.RETURN)

        time.sleep(8)

        # Wait for the bot to respond
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[aria-live="polite"]')))
        all_responses = driver.find_elements(By.CSS_SELECTOR, 'span[aria-live="off"]')
        bot_responses = driver.find_elements(By.CSS_SELECTOR, 'span[aria-live="polite"]')

        bot_text_responses = []
        for xd in all_responses:
            bot_text_responses.append(xd.text)

        for response in bot_responses:
            if response.text == "":
                pass
            else:
                print(colorama.Fore.GREEN + response.text)
                print(colorama.Fore.RESET)
                add_message(response.text, initial_time)
    except NoSuchElementException:
        try:
            time.sleep(4)
            # Find the image element by its CSS selector
            image_element = driver.find_elements(By.CSS_SELECTOR, 'img[data-testid="chat-message-image"]')
            # Get the value of the "src" attribute
            src = image_element[-1].get_attribute("src")

            # Display the link to the terminal
            add_message(src, initial_time)
            print(colorama.Fore.GREEN + src)
            print(colorama.Fore.RESET)


            print(colorama.Fore.RED + "Send another one / Stop:" + colorama.Fore.CYAN)
            message = input()
            if message == "Send another one":
                driver.find_element(By.XPATH, '//button[text()="Send another one"]').click()
                time.sleep(6)
            else:
                driver.find_element(By.XPATH, '//button[text()="Stop"]').click()
                print()
                time.sleep(6)
        except:
            print("ERROR: We do not find the textBox element. Exception:\tNoSuchElementException")
            pass

    '''if len(bot_responses) > 0:
        last_bot_response = bot_responses[-1]
        if last_bot_response.text != "":
            add_message(last_bot_response.text, initial_time)
            print(colorama.Fore.GREEN + last_bot_response.text)
            print(colorama.Fore.RESET)

        if len(bot_responses) > 1:
            additional_responses = bot_responses[:-1]
            for response in additional_responses:
                if response.text != "":
                    add_message(response.text, initial_time)'''


def add_message(message, initialtime):
    now = datetime.now()
    time = now.strftime("%H-%M-%S")
    date = now.strftime("%Y-%m-%d")
    repo_dir = os.path.join(os.path.abspath(__file__)[:-10].split("\n")[0], "conversations")

    if process_system.plat() == "Windows":
        x = repo_dir + "\\" + date
        filepath = x + "\\" + initialtime + ".txt"
    else:
        x = repo_dir + "/" + date
        filepath = x + "/" + initialtime + ".txt"
    if not os.path.exists(x):
        os.mkdir(x)

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(time.strip() + ": " + message.strip() + "\n")


def main():
    repo_dir = os.path.join(os.path.abspath(__file__)[:-10].split("\n")[0], "conversations")

    if not os.path.exists(repo_dir):
        os.mkdir(repo_dir)
    initial_time = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

    if len(sys.argv) == 2:
        try:
            replika(sys.argv[1])
            driver.quit()
        except:
            print("CLOSING...")
            driver.quit()
            exit(1)
    else:
        while True:
            print(colorama.Fore.RED + "Enter your text:" + colorama.Fore.CYAN)
            replika(input())


if __name__ == '__main__':
    main()
