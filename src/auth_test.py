
'''
Tests for auth.py

All tests are written assuming that the pretend database will be the same database used by all functions.
For example, in the first test 'test_valid_email()', john is registered. For all other tests, john 
will exist in the pretend databse. If john tries to register again it will raise an error
'''

import pytest
import auth
from error import InputError


def test_valid_email():
    auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')


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
    auth.auth_register('bob1@gmail.com', 'qwe123!@#', 'Bob', 'Smith')


def test_invalid_password():
    with pytest.raises(InputError) as e:
        auth.auth_register('john1@gmail.com', 'ddd', 'John', 'Smith')
    assert 'Password too short' == str(e.value)

    with pytest.raises(InputError) as e:
        auth.auth_register('john2@gmail.com', '', 'John', 'Smith')
    assert 'Password too short' == str(e.value)


def test_valid_name_first():
    auth.auth_register('john3@gmail.com', 'qwe123!@#', 'John', 'Smith')


def test_invalid_name_first():
    with pytest.raises(InputError) as e:
        auth.auth_register('john4@gmail.com', 'qwe123!@#',
                           'adsfkhsafhasklfhsklajfhsklajfhklsahfklashfklashfjklshaklfhasdklfhsadkljfhsadklfhasklhfklsahfklsadhfklasdhfklasdhfkljs', 'Smith')
    assert 'First Name too long or short' == str(e.value)

    with pytest.raises(InputError) as e:
        auth.auth_register('john4@gmail.com', 'qwe123!@#',
                           '', 'Smith')
    assert 'First Name too long or short' == str(e.value)


def test_valid_name_last():
    auth.auth_register('john5@gmail.com', 'qwe123!@#', 'John', 'Smith')


def test_invalid_name_last():
    with pytest.raises(InputError) as e:
        auth.auth_register('john6@gmail.com', 'qwe123!@#',
                           'John', 'adsfkhsafhasklfhsklajfhsklajfhklsahfklashfklashfjklshaklfhasdklfhsadkljfhsadklfhasklhfklsahfklsadhfklasdhfklasdhfkljs')
    assert 'Last Name too long or short' == str(e.value)

    with pytest.raises(InputError) as e:
        auth.auth_register('john6@gmail.com', 'qwe123!@#',
                           'John', '')
    assert 'Last Name too long or short' == str(e.value)


def test_registered_login():
    auth.auth_login('john@gmail.com', 'qwe123!@#')


def test_incorrect_email_login():
    with pytest.raises(InputError) as e:
        auth.auth_login('bob99@gmail.com', 'qwe123!@#')
    assert 'Incorrect email' == str(e.value)


def test_incorrect_password_login():

    with pytest.raises(InputError) as e:
        auth.auth_login('john@gmail.com', 'dfdfdf!@#')
    assert 'Incorrect password' == str(e.value)


def test_logout_success():
    login = auth.auth_login('john@gmail.com', 'qwe123!@#')
    logout = auth.auth_logout(login['token'])
    assert logout['is_success'] == True


def test_logout_fail():
    login = auth.auth_login('john@gmail.com', 'qwe123!@#')
    logout = auth.auth_logout(login['token'] + 'avc')
    assert logout['is_success'] == False
