from login import *


if __name__ == "__main__":
    user_name = "khmais"
    password = "poussword"
    number_emails = 1

    selenium,chrome_driver = initiate_automator()

    #login(selenium,chrome_driver,number_emails,user_name,password)
    selenium.open_text_to_speech_page()
    selenium.youtube_to_text("hello","Arabic (Tunisia)","Off","Off","Off")

    #selenium.close_browser(chrome_driver)
    '''
    #test
    email = "07g94u2q4k@rteet.com"
    print(email)
    login_domain_tuple = split_email(email)
    response = retrieve_mail(login_domain_tuple)
    print(response)

    verification_code = retrieve_code(response)
    print(verification_code)
        '''
        
