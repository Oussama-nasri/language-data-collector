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

def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("Successfully fetched the page!\n")
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    else:
        print("Failed to retrieve the page")



'""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""'

# Set up logging
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

# Set username.
user = getpass.getuser()

# Define a Selenium class to automate the browser.
class Selenium:
    # Constructor method.
    def __init__(self, driver):
        self.driver = driver

    def extract_book(self,url):
        self.driver.get(url)
        time.sleep(10)
        book_content=[]
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        """book_content = soup.find_all("div", class_="textLayer")
        book_content=[text.get_text() for text in book_content]"""
        # Find the parent <div> with the class "page-selector"
        number_div = soup.find('div', class_='page-selector')

        # Find the <span> within this <div> and extract its text
        number_pages = int(number_div.find('span').text)


        
        for i in range(1,number_pages):
            page_div = soup.find('div', {'class': 'page', 'data-page-number': i})
            page_content = soup.find_all("div", class_="textLayer")
            
            
            page_content=[text.get_text()+' ' for text in page_content]
            book_content.extend(page_content)
        '''except:
            book_content=[]
            print("no pages in the book!")'''

        return book_content
        

    # Method to open jstor in Chrome.
    def open_login_page(self):
        self.driver.get("https://voiser.net/log-in")
        time.sleep(5)
    


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
        # Wait for the shadow host element to be present
        time.sleep(5)     

        button = driver.find_element(By.ID, "loginMail")  # Replace with the actual button's ID

        # Step 3: Click the button
        button.click()
        
        print("\nlogin-------------\n")
        time.sleep(5)   
        # Enter the email
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "loginInputMail"))
        )
        email_input.send_keys(email)
        time.sleep(1) 
        print("\nloginnnnnnn-------------\n")

        button = driver.find_element(By.ID, "loginNext")  # Replace with the actual button's ID

        # Step 3: Click the button
        button.click()
        time.sleep(7) 
        #To do Catch error later in case of invalid email
        
        #Fill name 
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
        code_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "loginInputName"))
        )
        time.sleep(10)
        code_input.send_keys(verification_code)
        time.sleep(10)
        #To fix this function


def initiate_automator():
    # Kill any existing Chrome instances to avoid conflicts
    os.system("taskkill /im chrome.exe /f")

    user = getpass.getuser()

    service = Service()

    options = webdriver.ChromeOptions()
    options.add_argument(
        f"--user-data-dir=C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data",
        
    )

    options.add_argument("--profile-directory=Profile 2")
    options.add_argument("--start-maximized")

    chrome_driver = uc.Chrome(options=options)

    selenium = Selenium(driver=chrome_driver)

    return selenium,chrome_driver

if __name__ == "__main__":
    email = "hh.com"
    verification_code = "5555"
    selenium,chrome_driver = initiate_automator()

    selenium.open_login_page()

    selenium.log_in(chrome_driver,"salit",email,"pass")
    
    selenium.verify(verification_code)

    selenium.close_browser(chrome_driver)