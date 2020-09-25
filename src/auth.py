from data import data
import re
import pytest

# The following regex and def check(email) function was from geek for greek website
# https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
# Make a regular expression 
# for validating an Email 
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
# Define a function for 
# for validating an Email 
def check(email):  
    # pass the regular expression 
    # and the string in search() method 
    if(re.search(regex,email) != 0):  
        # print("Valid Email")
        return 1
          
    else:  
        # print("Invalid Email")  
        return 0

def auth_login(email, password):
    return {
        'u_id': 1,
        'token': '12345',
    }

def auth_logout(token):
    return {
        'is_success': True,
    }

def auth_register(email, password, name_first, name_last):
    # checks for valid email
    if check(email) == 0:
        raise NameError("Invalid email")

    # Checks for repeated email
    user = data['users'] # user is now the list of dictonary of users
    #print(user)

    existing_emails = [ email_list['email'] for email_list in user] # creates a list of existing emails
    # above line from https://www.geeksforgeeks.org/python-get-values-of-particular-key-in-list-of-dictionaries/
    #print (existing_emails)

    for old_emails in existing_emails:
        #print(old_emails)
        if email == old_emails: 
            raise NameError("Email already registered")
    
    if len(password) < 6:
        raise NameError("Password too short")

    if len(name_first) < 1 or len(name_first) > 50:
        raise NameError("First Name too long or short")

    if len(name_last) < 1 or len(name_last) > 50:
        #try:
        raise NameError("Last Name too long or short")
        #except NameError:
        #    print("Last_name exception ignored")
        #    raise
        #these commented out sections are for if you wasnt to ingore the errors

    handle = name_first + name_last
    if len(handle) > 20: # keeping the handle under 20 chars
        handle = handle[0:20]
    # creating a new dictionary for new user
    new_user = {
        'u_id': len(user),
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle,
    }
    user.append(new_user)
    print(f"{new_user}")

    return {
        'u_id': 1,
        'token': '12345',
    }

auth_register('johdsn@gmail.com', 'qwe123!@#', 'John0', 'Smith')

auth_register('jwqegfgaohn@gmail.com', 'qwe1236!@#', 'John13', 'Smith')
auth_register('jwqegvcxvohn@gmail.com', 'qwe1236!@#', 'John14', 'Smith')
auth_register('johdsadsn@gmail.com', '1234567', 'asasfgasgsadf', '123456789101112dasdf')

