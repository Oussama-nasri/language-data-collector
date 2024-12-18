import selenium
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import getpass
import os
import time
import logging
import undetected_chromedriver as uc
import tempfile



# Set up logging
def logg():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler("Voiser", mode="a")
    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - [%(levelname)s] [%(pathname)s:%(lineno)d] - %(message)s - [%(process)d:%(thread)d]"
    )
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    print = logger.info
    return print



# Define a Selenium class to automate the browser.
class Selenium:
    # Constructor method.
    def __init__(self, driver):
        self.driver = driver


    # Method to open voiser in Chrome.
    def open_login_page(self):
        self.driver.get("https://voiser.net/log-in")
        time.sleep(10)
    


    # Method to close the Chrome instance.
    def close_browser(self, driver):
        """
        Closes the web browser.

        Args:
        driver (selenium.webdriver.Chrome): The Chrome web driver object.

        Returns:
        None
        """
        self.driver.quit()

    def log_in(self,driver,name,email,password):

        time.sleep(5)     

        button = driver.find_element(By.ID, "loginMail")

        button.click()
        
        print("\n-------------Login-------------\n")
        time.sleep(5)   
        # Enter the email
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "loginInputMail"))
        )
        email_input.send_keys(email)
        time.sleep(1) 
        print("\n-------------Regiser coordinates-------------\n")

        button = driver.find_element(By.ID, "loginNext")

        button.click()
        time.sleep(7) 
        #To do Catch error later in case of invalid email
        
        #Fill Name
        name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "loginInputName"))
        )
        name_input.send_keys(name)

        #Fill Password
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "loginInputPassword"))
        )
        password_input.send_keys(password)

        time.sleep(1) 
        #Click login botton

        button = driver.find_element(By.ID, "loginNext")  # Replace with the actual button's ID

        # Step 3: Click the button
        button.click()
        time.sleep(10)

    def verify(self,driver,verification_code):
        # Find the input fields
        code_inputs = driver.find_elements(By.CLASS_NAME, "code-input")

        # Ensure there are exactly 4 input fields
        if len(code_inputs) != 4:
            print("Error: Found a different number of input fields than expected.")
            return

        # Directly inject the values into the input fields using JavaScript
        for i, digit in enumerate(str(verification_code)):
            driver.execute_script(f"arguments[0].value = '{digit}';", code_inputs[i])

        # Manually trigger the 'input' event to notify JavaScript
        for input_field in code_inputs:
            driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles: true}));", input_field)
        
        print("Verification code sent successfully!")

        button = driver.find_element(By.ID, "loginVerifyButton")  

        button.click()
        time.sleep(7) 
        
    def open_text_to_speech_page(self):
        self.driver.get("https://voiser.net/account/speech-to-text/")
        time.sleep(10)
    
    def youtube_to_text(self):
        #select youtube tab
        tab = self.driver.find_element(By.CLASS_NAME, "card-transcribe-youtube")
        tab.click()
        time.sleep(10)

def initiate_automator():
    # Kill any existing Chrome instances to avoid conflicts
    os.system("taskkill /im chrome.exe /f")
    # Fetch current user's name
    user = getpass.getuser()


    # Define Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument(
        f"--user-data-dir=C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data",
        
    )
    options.add_argument("--profile-directory=Profile 2")
    options.add_argument("--start-maximized")

    chrome_driver = uc.Chrome(options=options)
    selenium = Selenium(driver=chrome_driver)
    '''
    options = webdriver.ChromeOptions()

    temp_profile = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_profile}")

    
    chrome_driver = uc.Chrome(options=options)
    chrome_driver.set_window_size(800,800)
    selenium = Selenium(driver=chrome_driver)
    '''
    return selenium,chrome_driver

if __name__ == "__main__":
    pass