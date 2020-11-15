'''
26/9/2020
Tests for user.py
'''

import pytest
import auth
from error import InputError
from other import clear, users_all


def test_successful_registration():
    '''
    Test registration, login and logout working
    '''

    auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    login = auth.auth_login('john@gmail.com', 'qwe123!@#')
    logout = auth.auth_logout(login['token'])
    assert logout['is_success'] == True
    clear()


def test_invalid_email():
    '''
    Test that InputError is thrown for invalid email input
    '''

    with pytest.raises(InputError) as e:
        auth.auth_register('john.com', 'qwe123!@#', 'John', 'Smith')
    assert '400 Bad Request: Invalid email' == str(e.value)

    with pytest.raises(InputError) as e:
        auth.auth_register('', 'qwe123!@#', 'John', 'Smith')
    assert '400 Bad Request: Invalid email' == str(e.value)
    clear()


def test_email_already_registered():
    '''
    Test that InputError is thrown is user is trying to register
    with email that has already been registered
    '''

    auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    with pytest.raises(InputError) as e:
        auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    assert '400 Bad Request: Email already registered' == str(e.value)
    clear()


def test_invalid_password():
    '''
    Test InputError is thrown when length of password entered
    is too short (less than 6 characters)
    '''

    with pytest.raises(InputError) as e:
        auth.auth_register('john@gmail.com', 'q3!@#', 'John', 'Smith')
    assert '400 Bad Request: Password too short' == str(e.value)
    clear()


def test_invalid_name_first():
    '''
    Test InputError is thrown when length of first entered
    is not between 1 and 50 characters
    '''

    with pytest.raises(InputError) as e:
        auth.auth_register('john@gmail.com', 'qwe123!@#',
                           'adsfkhsafhasklfhsklajfhsklajfhklsahfklashfklashfjklshaklfhasdklfhsadkljfhsadklfhasklhfklsahfklsadhfklasdhfklasdhfkljs', 'Smith')
    assert '400 Bad Request: First Name too long or short' == str(e.value)

    with pytest.raises(InputError) as e:
        auth.auth_register('john@gmail.com', 'qwe123!@#',
                           '', 'Smith')
    assert '400 Bad Request: First Name too long or short' == str(e.value)
    clear()


def test_invalid_name_last():
    '''
    Test InputError is thrown when length of last name entered
    is not between 1 and 50 characters
    '''

    with pytest.raises(InputError) as e:
        auth.auth_register('john@gmail.com', 'qwe123!@#',
                           'John', 'adsfkhsafhasklfhsklajfhsklajfhklsahfklashfklashfjklshaklfhasdklfhsadkljfhsadklfhasklhfklsahfklsadhfklasdhfklasdhfkljs')
    assert '400 Bad Request: Last Name too long or short' == str(e.value)

    with pytest.raises(InputError) as e:
        auth.auth_register('john@gmail.com', 'qwe123!@#',
                           'John', '')
    assert '400 Bad Request: Last Name too long or short' == str(e.value)
    clear()


def test_incorrect_email_login():
    '''
    Test that InputError is throw for login where email has not been
    registered yet
    '''

    auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    with pytest.raises(InputError) as e:
        auth.auth_login('bob99@gmail.com', 'qwe123!@#')
    assert '400 Bad Request: Email does not belong to a user' == str(e.value)
    clear()


def test_incorrect_password_login():
    '''
    Test that InputError is throw for login where password
    is incorrect
    '''

    auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    with pytest.raises(InputError) as e:
        auth.auth_login('john@gmail.com', 'dfdfdf!@#')
    assert '400 Bad Request: Incorrect password' == str(e.value)
    clear()




def test_handle_too_long():
    '''
    Test handle large number of characters
    '''

    user = auth.auth_register(
        "john@gmail.com", "qwe123!@#", "1234567890", "yoyoy123456789")
    usersall_response = users_all(user["token"])
    handle = usersall_response["users"][0]["handle_str"]
    assert handle == "1234567890yoyoy12345"
    clear()


def test_invalid_code(): 
    '''
    Test invalid reset code
    '''
    auth.auth_register(
        "john@gmail.com", "qwe123!@#", "John", "Smith")
    
    with pytest.raises(InputError) as e:
        auth.auth_passwordreset_reset("123", "hjdashdads")
    assert '400 Bad Request: Invalid reset code' == str(e.value)
    clear()
