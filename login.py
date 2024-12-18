from auto_login import *
from automate import *

def login(selenium,chrome_driver,number_emails,user_name,password):
    email = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count={}".format(number_emails)).text
    
    email_list = str_to_list(email)
    for email in email_list:
        login_domain_tuple = split_email(email)
        
        print(email)
        
        selenium.open_login_page()

        selenium.log_in(chrome_driver,user_name,email,password)

        response = retrieve_mail(login_domain_tuple)
        while response is None:
            print(response)
            print("Waiting for email...")
            time.sleep(5)  
            response = retrieve_mail(login_domain_tuple)
            print(response)
            print("-----------y----------")
        print("Response : \n",response)

        verification_code = retrieve_code(response)
        print("verification_code : \n",verification_code)
        selenium.verify(chrome_driver,verification_code)

