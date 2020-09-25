'''
Tests for auth.py
'''

import pytest
import auth
from testing_variables import *


def test_valid_email():
    result = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    assert result['token'] == '12345'


def test_invalid_email():
    with pytest.raises(InputError) as e:
        auth.auth_register('john.com', 'qwe123!@#', 'John', 'Smith')
    assert 'Invalid email' == str(e.value)

    with pytest.raises(InputError) as e:
        auth.auth_register('', 'qwe123!@#', 'John', 'Smith')
    assert 'Invalid email' == str(e.value)


def test_email_already_registered():
    auth.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Smith')
    with pytest.raises(InputError) as e:
        auth.auth_register('bob@gmail.com', 'qwe123!@#', 'John', 'Smith')
    assert 'Email already registered' == str(e.value)


def test_valid_password():
    result = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    assert result['token'] == '12345'


def test_invalid_password():
    with pytest.raises(InputError) as e:
        auth.auth_register('john@gmail.com', 'ddd', 'John', 'Smith')
    assert 'Invalid password' == str(e.value)

    with pytest.raises(InputError) as e:
        auth.auth_register('john@gmail.com', '', 'John', 'Smith')
    assert 'Invalid password' == str(e.value)


def test_valid_name_first():
    result = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    assert result['token'] == '12345'


def test_invalid_name_first():
    with pytest.raises(InputError) as e:
        auth.auth_register('john@gmail.com', 'qwe123!@#',
                           'adsfkhsafhasklfhsklajfhsklajfhklsahfklashfklashfjklshaklfhasdklfhsadkljfhsadklfhasklhfklsahfklsadhfklasdhfklasdhfkljs', 'Smith')
    assert 'Invalid first name' == str(e.value)

    with pytest.raises(InputError) as e:
        auth.auth_register('john@gmail.com', 'qwe123!@#',
                           '', 'Smith')
    assert 'Invalid first name' == str(e.value)


def test_valid_name_last():
    result = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    assert result['token'] == '12345'


def test_invalid_name_last():
    with pytest.raises(InputError) as e:
        auth.auth_register('john@gmail.com', 'qwe123!@#',
                           'John', 'adsfkhsafhasklfhsklajfhsklajfhklsahfklashfklashfjklshaklfhasdklfhsadkljfhsadklfhasklhfklsahfklsadhfklasdhfklasdhfkljs')
    assert 'Invalid last name' == str(e.value)

    with pytest.raises(InputError) as e:
        auth.auth_register('john@gmail.com', 'qwe123!@#',
                           'John', '')
    assert 'Invalid last name' == str(e.value)


def test_registered_login():
    result = auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    auth.auth_login('john@gmail.com', 'qwe123!@#')
    assert result['token'] == '12345'


def test_incorrect_email_login():
    auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    with pytest.raises(InputError) as e:
        auth.auth_login('bob@gmail.com', 'qwe123!@#')
    assert 'Incorrect email' == str(e.value)


def test_incorrect_password_login():
    auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    with pytest.raises(InputError) as e:
        auth.auth_login('john@gmail.com', 'dfdfdf!@#')
    assert 'Incorrect email' == str(e.value)


def test_logout():
    auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    login = auth.auth_login('john@gmail.com', 'qwe123!@#')
    logout = auth.auth_logout(login['token'])

    assert logout['is_success'] == True
