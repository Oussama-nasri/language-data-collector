from auto_login import *
from automate import *


if __name__ == "__main__":
    number_emails = 1
    email = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count={}".format(number_emails)).text
    
    email_list = str_to_list(email)
    for email in email_list:
        login_domain_tuple = split_email(email)
        
        print(email)
        
        

        selenium,chrome_driver = initiate_automator()

        selenium.open_login_page()

        selenium.log_in(chrome_driver,"salit",email,"pass")

        response = retrieve_mail(login_domain_tuple)
        while response is None:
            print("Waiting for email...")
            time.sleep(1)  # Wait for 1 second before checking again
            response = retrieve_mail(login_domain_tuple)
        print("Response : \n",response)

        verification_code = retrieve_code(response)
        print("verification_code : \n",verification_code)
        selenium.verify(chrome_driver,verification_code)

        selenium.close_browser(chrome_driver)
        '''
        #test
        print(email)
        login_domain_tuple = split_email(email)
        response = retrieve_mail(login_domain_tuple)
        print(response)

        verification_code = retrieve_code(response)
        print(verification_code)
        
        '''
