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
from selenium.common.exceptions import TimeoutException
import random
import subprocess



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
        time.sleep(10) 
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
        time.sleep(5)
        print("----skipping----")
        self.skip_instruction_panels()
        print("----skipped----")
    
    def wait_till_ready(self, flag):
        print("---Processing has began---")
        while True:
            try:
                # Set up an explicit wait with no timeout, it will check for the element continuously
                wait = WebDriverWait(self.driver, 5)
                
                # Wait for the element to become visible that contains the flag
                wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, f"//td[contains(., '{flag}')]")
                    )
                )
                
                return True

            except TimeoutException:
                print("Please wait! ------ Processing your video!")
                
    
    def click_ok_estimate_duration(self):
        time.sleep(20)
        estimation = self.driver.find_element(By.ID, "swal2-content").text
        button = self.driver.find_element(By.CLASS_NAME, "swal2-confirm")
        button.click()
        return estimation
    
    def skip_instruction_panels(self):
        # Create an ActionChains object and perform a click at the random position
        action = ActionChains(self.driver)
        action.move_by_offset(0, 0).click().perform()

        # Wait a bit to ensure the click happens
        time.sleep(1)
    
    def translate(self,tanslation_language):
        if tanslation_language!=None:
            language_dropbox = self.driver.find_element(By.CLASS_NAME, "select2-selection__rendered")
            language_dropbox.click()
            time.sleep(2)
            language = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//li[contains(., '{}')]".format(tanslation_language))))
            language.click()
            time.sleep(2)

    def progress_bar(self):
        print("----Beginning Translation----")
        while True:
            # Locate the progress bar element
            progress_bar = self.driver.find_element(By.ID, "upload_percent")
            
            # Retrieve the value of the 'style' attribute to get the width
            style_attribute = progress_bar.get_attribute("style")
            
            # Extract the percentage from the style (the width in the style attribute)
            progress_percentage = style_attribute.split(":")[1].split("%")[0]
            
            # Print the current progress percentage
            print(f"Progress: {progress_percentage}%")
            
            # Break the loop if progress reaches 100%
            if (int(progress_percentage) >= 100) or (int(progress_percentage) == 0):
                print("Translation complete!")
                break
            
            time.sleep(30)

    
    def download_text_file(self):

        download_button = self.driver.find_element(By.ID, "download-file-button")
        download_button.click()
        text_files = self.driver.find_elements(By.XPATH, "//button[contains(., 'Text File (.txt)')]")

        for text_file in text_files:
            text_file.click()
            time.sleep(15)
            download_button.click()
        download_button.click()
        time.sleep(2)
    
        

    def youtube_to_text(self,youtube_url,language_variable,ponctuation_variable,profanity_variable,speaker_variable,tanslation_language=None):
        #select youtube tab
        tab = self.driver.find_element(By.CLASS_NAME, "card-transcribe-youtube")
        tab.click()
        time.sleep(1)
        #Add youtube link
        youtube_input = WebDriverWait(self.driver, 2).until(
            EC.presence_of_element_located((By.ID, "upload_from_youtube"))
        )
        youtube_input.send_keys(youtube_url)
        time.sleep(2)
        #Change language
        language_dropbox = self.driver.find_element(By.CLASS_NAME, "select2-selection--single")
        language_dropbox.click()
        time.sleep(2)
        language = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//li[contains(., '{}')]".format(language_variable))))
        language.click()
        time.sleep(2)
        #Change ponctuation
        ponctuation_dropbox = self.driver.find_element(By.ID, "select2-filterPunctuation-container")
        ponctuation_dropbox.click()
        time.sleep(2)
        ponctuation = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//li[contains(., 'Punctuation: {}')]".format(ponctuation_variable))))
        ponctuation.click()
        time.sleep(2)
        #Change profanity
        profanity_dropbox = self.driver.find_element(By.ID, "select2-filterProfanity-container")
        profanity_dropbox.click()
        time.sleep(2)
        profanity = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//li[contains(., 'Profanity Filter: {}')]".format(profanity_variable))))
        profanity.click()
        time.sleep(2)
        #Speaker recognition
        speaker_dropbox = self.driver.find_element(By.ID, "select2-filterSpeaker-container")
        speaker_dropbox.click()
        time.sleep(2)
        speaker = WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable((By.XPATH, "//li[contains(., 'Speaker Recognition {}')]".format(speaker_variable))))
        speaker.click()
        time.sleep(2)
        #Convert audio to txt button
        button = self.driver.find_element(By.ID, "run_form")
        button.click()
        time.sleep(2)
        #Click on OK button
        estimation = self.click_ok_estimate_duration()
        time.sleep(5)
        print(estimation)
        #Skipping 
        self.skip_instruction_panels()
        #waiting for status complete
        self.wait_till_ready(" Completed")
        time.sleep(2)
        
        #Get donwload page
        download_page_link = self.driver.find_element(By.XPATH, "//td[@class='cursor-pointer']/a").get_attribute("href")
        print(download_page_link)
        #Go to the download page
        self.driver.get(download_page_link)
        time.sleep(20)
        #Translate to english
        self.skip_instruction_panels()
        self.translate(tanslation_language)
        self.skip_instruction_panels()
        self.progress_bar()
        self.download_text_file()
        print("120 seconds and closing")
        time.sleep(120)





def initiate_automator():
    # Kill any existing Chrome instances to avoid conflicts
    os.system("taskkill /im chrome.exe /f")
    """# Fetch current user's name
    user = getpass.getuser()


    # Define Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument(
        f"--user-data-dir=C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data",
        
    )
    options.add_argument("--profile-directory=Profile 2")
    options.add_argument("--start-maximized")
    chrome_driver = webdriver.Chrome(options=options)
    selenium = Selenium(driver=chrome_driver)
    """
    

    #Set download folder 
    download_folder = r"C:\Users\Administrator\Desktop\voiser-proj\download\\"

    # Ensure the folder exists
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    command = f'icacls "{download_folder}" /grant Everyone:F'
    subprocess.run(command, shell=True)

    prefs = {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "savefile.default_directory": download_folder
    }

    
    
    options = webdriver.ChromeOptions()

    temp_profile = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_profile}")

    options.add_experimental_option("prefs", prefs)

    
    chrome_driver = webdriver.Chrome(options=options)
    chrome_driver.set_window_size(1336,768)
    selenium = Selenium(driver=chrome_driver)
    
    return selenium,chrome_driver

if __name__ == "__main__":
    pass