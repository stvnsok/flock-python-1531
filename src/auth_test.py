'''
Tests for user.py

'''
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import pytest
import helper_test_functions as test_setup

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


def test_successful_registration(url):
    '''
    Test registration, login and logout working
    '''
    test_setup.auth_register(
        "john@gmail.com", "qwe123!@#", "John", "Smith", url)

    login_response = test_setup.auth_login("john@gmail.com", "qwe123!@#", url)

    logout_response = test_setup.auth_logout(login_response["token"], url)

    assert logout_response["is_success"]

    test_setup.clear(url)


def test_invalid_email(url):
    '''
    Test that InputError is thrown for invalid email input
    '''

    error_response = test_setup.auth_register(
        "john.com", "qwe123!@#", "John", "Smith", url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Invalid email</p>"

    test_setup.clear(url)


def test_email_already_registered(url):
    '''
    Test that InputError is thrown is user is trying to register
    with email that has already been registered
    '''

    test_setup.auth_register(
        "john@gmail.com", "qwe123!@#", "John", "Smith", url)

    error_response = test_setup.auth_register(
        "john@gmail.com", "qwe123!@#", "John", "Smith", url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Email already registered</p>"

    test_setup.clear(url)


def test_invalid_password(url):
    '''
    Test InputError is thrown when length of password entered
    is too short (less than 6 characters)
    '''

    error_response = test_setup.auth_register(
        "john@gmail.com", "qwe",  "John", "Smith", url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Password too short</p>"

    test_setup.clear(url)


def test_invalid_name_first(url):
    '''
    Test InputError is thrown when length of first entered
    is not between 1 and 50 characters
    '''

    long_first_name = """adsfkhsafhasklfhsklajfhsklajfhklsahf
                        klashfklashfjklshaklfhasdklfhsadkljfhs
                        adklfhasklhfklsahfklsadhfklasdhfklasdhfkljs"""

    error_response = test_setup.auth_register(
        "john@gmail.com", "qwe123!@#", long_first_name, "Smith", url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>First Name too long or short</p>"

    error_response = test_setup.auth_register(
        "john@gmail.com", "qwe123!@#", "", "Smith", url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>First Name too long or short</p>"

    test_setup.clear(url)


def test_invalid_name_last(url):
    '''
    Test InputError is thrown when length of last name entered
    is not between 1 and 50 characters
    '''

    long_last_name = """adsfkhsafhasklfhsklajfhsklajfhklsahf
                        klashfklashfjklshaklfhasdklfhsadkljfhs
                        adklfhasklhfklsahfklsadhfklasdhfklasdhfkljs"""

    error_response = test_setup.auth_register(
        "john@gmail.com", "qwe123!@#", "John", long_last_name, url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Last Name too long or short</p>"

    error_response = test_setup.auth_register(
        "john@gmail.com", "qwe123!@#", "John", "", url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Last Name too long or short</p>"

    test_setup.clear(url)


def test_incorrect_email_login(url):
    '''
    Test that InputError is throw for login where email has not been
    registered yet
    '''

    error_response = test_setup.auth_login("bob@gmail.com", "qwe123!@#", url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Email does not belong to a user</p>"

    test_setup.clear(url)


def test_incorrect_password_login(url):
    '''
    Test that InputError is throw for login where password
    is incorrect
    '''
    test_setup.auth_register(
        "john@gmail.com", "qwe123!@#", "John", "Smith", url)

    error_response = test_setup.auth_login("john@gmail.com", "qwe12", url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Incorrect password</p>"

    test_setup.clear(url)


def test_logout_fail(url):
    '''
    Test that if an incorrect token is passed on logout
    correct error is passed to user
    '''

    test_setup.auth_register(
        "john@gmail.com", "qwe123!@#", "John", "Smith", url)

    test_setup.auth_login("john@gmail.com", "qwe123!@#", url)

    logout_response = test_setup.auth_logout("WrongToken", url)

    assert not logout_response["is_success"]

    test_setup.clear(url)


def test_handle_too_long(url):
    '''
    Test that handle is being created correctly
    '''

    register_response = test_setup.auth_register(
        "john@gmail.com", "qwe123!@#", "1234567890", "yoyoy123456789", url)

    # response = requests.get(f'{url}users/all', json={"token":register_response["token"]})

    usersall_response = test_setup.users_all(register_response["token"], url)

    handle = usersall_response["users"][0]["handle_str"]

    assert handle == "1234567890yoyoy12345"

    test_setup.clear(url)
