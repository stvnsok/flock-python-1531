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

# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
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
    
    requests.post(f'{url}auth/register', json={
        "email": "john@gmail.com", 
        "password": "qwe123!@#",
        "name_first": "John",
        "name_last": "Smith",
    })
    
    response = requests.post(f'{url}auth/login', json={
        "email": "john@gmail.com", 
        "password": "qwe123!@#",        
    })

    login_response = response.json()

    response = requests.post(f'{url}auth/logout', json={
        "token":login_response["token"]
    })

    logout_response = response.json()

    assert logout_response["is_success"] == True
    
    requests.delete(f'{url}/clear')



def test_invalid_email(url):
    '''
    Test that InputError is thrown for invalid email input
    '''

    response = requests.post(f'{url}auth/register', json={
        "email": "john.com", 
        "password": "qwe123!@#",
        "name_first": "John",
        "name_last": "Smith",
    })

    error_response = response.json()

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Invalid email</p>"

    requests.delete(f'{url}/clear')


def test_email_already_registered(url):
    '''
    Test that InputError is thrown is user is trying to register
    with email that has already been registered
    '''

    response = requests.post(f'{url}auth/register', json={
        "email": "john@gmail.com", 
        "password": "qwe123!@#",
        "name_first": "John",
        "name_last": "Smith",
    })
    
    response = requests.post(f'{url}auth/register', json={
        "email": "john@gmail.com", 
        "password": "qwe123!@#",
        "name_first": "John",
        "name_last": "Smith",
    })
    
    error_response = response.json()

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Email already registered</p>"

    requests.delete(f'{url}/clear')


def test_invalid_password(url):
    '''
    Test InputError is thrown when length of password entered
    is too short (less than 6 characters)
    '''

    response = requests.post(f'{url}auth/register', json={
        "email": "john@gmail.com", 
        "password": "qwe",
        "name_first": "John",
        "name_last": "Smith",
    })
    
    error_response = response.json()

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

    response = requests.post(f'{url}auth/register', json={
        "email": "john@gmail.com", 
        "password": "qwe123!@#",
        "name_first": long_first_name,
        "name_last": "Smith",
    })
    
    error_response = response.json()

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>First Name too long or short</p>"

    response = requests.post(f'{url}auth/register', json={
        "email": "john@gmail.com", 
        "password": "qwe123!@#",
        "name_first": "",
        "name_last": "Smith",
    })
    
    error_response = response.json()

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

    response = requests.post(f'{url}auth/register', json={
        "email": "john@gmail.com", 
        "password": "qwe123!@#",
        "name_first": "John",
        "name_last": long_last_name,
    })
    
    error_response = response.json()

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Last Name too long or short</p>"

    response = requests.post(f'{url}auth/register', json={
        "email": "john@gmail.com", 
        "password": "qwe123!@#",
        "name_first": "John",
        "name_last": "",
    })
    
    error_response = response.json()

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Last Name too long or short</p>"

    requests.delete(f'{url}/clear')    



def test_incorrect_email_login(url):
    '''
    Test that InputError is throw for login where email has not been
    registered yet
    '''

    response = requests.post(f'{url}auth/login', json={
        "email": "bob@gmail.com", 
        "password": "qwe123!@#",
    })

    error_response = response.json()

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
    requests.post(f'{url}auth/register', json={
        "email": "john@gmail.com", 
        "password": "qwe123!@#",
        "name_first": "John",
        "name_last": "Smith",
    })
    
    requests.post(f'{url}auth/login', json={
        "email": "john@gmail.com", 
        "password": "qwe123!@#",        
    })

    response = requests.post(f'{url}auth/logout', json={
        "token":"wrong token"
    })

    logout_response = response.json()

    assert logout_response["is_success"] == False
    
    requests.delete(f'{url}/clear')

def test_handle_too_long(url):
    '''
    Test that handle is being created correctly
    '''
    response = requests.post(f'{url}auth/register', json={
        "email": "john@gmail.com", 
        "password": "qwe123!@#",
        "name_first": "1234567890",
        "name_last": "yoyoy123456789",
    })

    register_response = response.json()

    response = requests.get(f'{url}users/all', json={"token":register_response["token"]})

    usersall_response = response.json()

    handle = usersall_response["users"][0]["handle_str"]

    assert handle == "1234567890yoyoy12345"

    requests.delete(f'{url}/clear')

    