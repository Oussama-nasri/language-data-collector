import requests
import re


number_emails = 10

#print(requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count={}".format(number_emails)).text)

#we need to benchmark the average wait time
#print(requests.get("https://www.1secmail.com/api/v1/?action=getMessages&login=26fah1o7kd&domain=rteet.com").text)

def split_email(email):
    pattern = r"([^@]+)@(.+)"
    match = re.match(pattern, email)
    if match:
        local_part = match.group(1)
        domain = match.group(2)
        return local_part, domain
    else:
        return None, None
    
def retrieve_mail(login_domain_tuple):
    #Obtain the content of the recieved emails in list format
    response = requests.get("https://www.1secmail.com/api/v1/?action=getMessages&login={}&domain={}".format(login_domain_tuple[0],login_domain_tuple[1])).text
    if response!="[]":
        return response
    else:
        return None
    

def str_to_list(string):
    #Transforms the list from being in string format into an actual list
    pattern = r'"(.*?)"'
    matches = re.findall(pattern, string)
    
    return matches

def retrieve_code(response):
    pattern = r'(?<=Verify Your Account - )\d{4}(?= - Voiser.net)'


    match = re.search(pattern, response)

    if match:
        number = match.group()  
        return number
    else:
        print("No number found")


if __name__ == "__main__":
    number_emails = 1
    email = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count={}".format(number_emails)).text
    email_list = str_to_list(email)
    for email in email_list:
        login_domain_tuple = split_email(email)
        response = retrieve_mail(login_domain_tuple)
        print(response)
