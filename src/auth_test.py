'''
Tests for auth.py

'''

import pytest
import auth
from error import InputError
from other import clear
from data import data


def test_successful_registration():
    auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    login = auth.auth_login('john@gmail.com', 'qwe123!@#')
    logout = auth.auth_logout(login['token'])
    assert logout['is_success'] == True
    clear()


def test_invalid_email():
    with pytest.raises(InputError) as e:
        auth.auth_register('john.com', 'qwe123!@#', 'John', 'Smith')
    assert 'Invalid email' == str(e.value)

    with pytest.raises(InputError) as e:
        auth.auth_login('animeanime.com', "password")
    assert 'Invalid email' == str(e.value)
    clear()


def test_email_already_registered():
    auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    with pytest.raises(InputError) as e:
        auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    assert 'Email already registered' == str(e.value)
    clear()


def test_invalid_password():
    with pytest.raises(InputError) as e:
        auth.auth_register('john@gmail.com', 'q3!@#', 'John', 'Smith')
    assert 'Password too short' == str(e.value)
    clear()


def test_invalid_name_first():
    with pytest.raises(InputError) as e:
        auth.auth_register('john@gmail.com', 'qwe123!@#',
                           'adsfkhsafhasklfhsklajfhsklajfhklsahfklashfklashfjklshaklfhasdklfhsadkljfhsadklfhasklhfklsahfklsadhfklasdhfklasdhfkljs', 'Smith')
    assert 'First Name too long or short' == str(e.value)

    with pytest.raises(InputError) as e:
        auth.auth_register('john@gmail.com', 'qwe123!@#',
                           '', 'Smith')
    assert 'First Name too long or short' == str(e.value)
    clear()


def test_invalid_name_last():
    with pytest.raises(InputError) as e:
        auth.auth_register('john@gmail.com', 'qwe123!@#',
                           'John', 'adsfkhsafhasklfhsklajfhsklajfhklsahfklashfklashfjklshaklfhasdklfhsadkljfhsadklfhasklhfklsahfklsadhfklasdhfklasdhfkljs')
    assert 'Last Name too long or short' == str(e.value)

    with pytest.raises(InputError) as e:
        auth.auth_register('john@gmail.com', 'qwe123!@#',
                           'John', '')
    assert 'Last Name too long or short' == str(e.value)
    clear()


def test_incorrect_email_login():
    auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    with pytest.raises(InputError) as e:
        auth.auth_login('bob99@gmail.com', 'qwe123!@#')
    assert 'Incorrect email' == str(e.value)
    clear()


def test_incorrect_password_login():
    auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    with pytest.raises(InputError) as e:
        auth.auth_login('john@gmail.com', 'dfdfdf!@#')
    assert 'Incorrect password' == str(e.value)
    clear()


def test_logout_fail():
    auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    login = auth.auth_login('john@gmail.com', 'qwe123!@#')
    logout = auth.auth_logout(login['token'] + 'avc')
    assert logout['is_success'] == False
    clear()

def test_handle_too_long():
    auth.auth_register('john@gmail.com', 'qwe123!@#', '1234567890', 'yoyoy123456789')
    users = data['users']
    handle = users[0]['handle_str']
    assert handle == "1234567890yoyoy12345"
    clear()
    