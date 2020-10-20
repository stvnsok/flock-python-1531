'''
Tests for user.py

'''
import pytest
import auth
from error import InputError
from other import clear
from data import data
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
import pytest
import server
from helper_test_functions import *

# # Helper function to set up user
# def register_user(email, password, name_first, name_last, url):
#     response = requests.post(f'{url}auth/register', json={
#         "email": "john@gmail.com", 
#         "password": "qwe123!@#",
#         "name_first": "John",
#         "name_last": "Smith",
#     })

#     return response.json()

# Fixture to get the URL of the server. 
@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")
    

'''
Tests for auth.py
'''
def test_successful_registration(url):
    '''
    Test registration, login and logout working
    '''
    register_user("john@gmail.com", "qwe123!@#", "John", "Smith", url)
    
    login_response = login_user("john@gmail.com", "qwe123!@#", url)

    logout_response = logout_user(login_response["token"], url) 

    assert logout_response["is_success"] == True
    
    requests.delete(f'{url}/clear')



def test_invalid_email(url):
    '''
    Test that InputError is thrown for invalid email input
    '''

    error_response = register_user("john.com", "qwe123!@#" , "John", "Smith", url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Invalid email</p>"

    requests.delete(f'{url}/clear')


def test_email_already_registered(url):
    '''
    Test that InputError is thrown is user is trying to register
    with email that has already been registered
    '''

    register_user("john@gmail.com", "qwe123!@#", "John", "Smith", url)
    
    error_response = register_user("john@gmail.com", "qwe123!@#", "John", "Smith", url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Email already registered</p>"

    requests.delete(f'{url}/clear')


def test_invalid_password(url):
    '''
    Test InputError is thrown when length of password entered
    is too short (less than 6 characters)
    '''
    
    error_response = register_user("john@gmail.com", "qwe",  "John", "Smith", url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Password too short</p>"

    requests.delete(f'{url}/clear')



def test_invalid_name_first(url):
    '''
    Test InputError is thrown when length of first entered
    is not between 1 and 50 characters
    '''

    long_first_name = """adsfkhsafhasklfhsklajfhsklajfhklsahf
                        klashfklashfjklshaklfhasdklfhsadkljfhs
                        adklfhasklhfklsahfklsadhfklasdhfklasdhfkljs"""

    
    error_response = register_user("john@gmail.com","qwe123!@#", long_first_name, "Smith" ,url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>First Name too long or short</p>"


    error_response = register_user("john@gmail.com","qwe123!@#", "", "Smith" ,url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>First Name too long or short</p>"

    requests.delete(f'{url}/clear')


def test_invalid_name_last(url):
    '''
    Test InputError is thrown when length of last name entered
    is not between 1 and 50 characters
    '''

    long_last_name = """adsfkhsafhasklfhsklajfhsklajfhklsahf
                        klashfklashfjklshaklfhasdklfhsadkljfhs
                        adklfhasklhfklsahfklsadhfklasdhfklasdhfkljs"""

    
    error_response = register_user("john@gmail.com","qwe123!@#", "John", long_last_name ,url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Last Name too long or short</p>"

    error_response = register_user("john@gmail.com","qwe123!@#", "John", "" ,url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Last Name too long or short</p>"

    requests.delete(f'{url}/clear')    



def test_incorrect_email_login(url):
    '''
    Test that InputError is throw for login where email has not been
    registered yet
    '''

    error_response = login_user("bob@gmail.com","qwe123!@#", url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Email does not belong to a user</p>"

    requests.delete(f'{url}/clear')    



def test_incorrect_password_login(url):
    '''
    Test that InputError is throw for login where password
    is incorrect
    '''
    
    requests.post(f'{url}auth/register', json={
        "email": "john@gmail.com", 
        "password": "qwe123!@#",
        "name_first": "John",
        "name_last": "Smith",
    })

    response = requests.post(f'{url}auth/login', json={
        "email": "john@gmail.com", 
        "password": "qwe12",
    })

    error_response = response.json()

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Incorrect password</p>"

    requests.delete(f'{url}/clear')  


def test_logout_fail(url):
    '''
    Test that if an incorrect token is passed on logout
    correct error is passed to user
    '''

    register_user("john@gmail.com", "qwe123!@#", "John", "Smith", url)

    login_user("john@gmail.com", "qwe123!@#", url)

    logout_response = logout_user("WrongToken", url)

    assert logout_response["is_success"] == False
    
    requests.delete(f'{url}/clear')

def test_handle_too_long(url):
    '''
    Test that handle is being created correctly
    '''

    register_response = register_user("john@gmail.com", "qwe123!@#", "1234567890", "yoyoy123456789", url)

    response = requests.get(f'{url}users/all', json={"token":register_response["token"]})

    usersall_response = response.json()

    handle = usersall_response["users"][0]["handle_str"]

    assert handle == "1234567890yoyoy12345"

    requests.delete(f'{url}/clear')

    