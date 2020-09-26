from data import *
import re
import pytest
from error import InputError

# The following regex and def check(email) function was from geek for greek website
# https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
# Make a regular expression
# for validating an Email
regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

'''
We should consider using user.py to create user instead of dictionary with register function
'''


def create_token(email):
    # creates a hash using in built python hash function
    return str(hash(email))


def check(email):
    # pass the regular expression
    # and checks format of email
    # return True is correct else False
    if(re.search(regex, email)):
        return True
    else:
        return False


def auth_login(email, password):

    # Check email is valid format
    if (check(email)) is not True:
        raise InputError('Invalided email')

    # Get users from data
    users = data['users']

    # Check that email and password are correct and valid
    for user in users:
        if (user['email'] != email):
            raise InputError('Incorrect email')
        if (user['email'] == email and user['password'] != password):
            raise InputError('Incorrect password')
        if (user['email'] == email and user['password'] == password):
            return {
                'u_id': user['u_id'],
                'token': user['token']
            }


def auth_logout(token):

    # Get users from data
    users = data['users']

    # Check that token exists
    for user in users:
        if (user['token'] == token):
            return {
                'is_success': True,
            }

    return {'is_success': False}


def auth_register(email, password, name_first, name_last):

    # checks for valid email
    if check(email) is not True:
        raise InputError('Invalid email')

    # Grabs all users from data
    users = data['users']

    # Cycles through all users to check if given email already exists
    for user in users:
        if user['email'] == email:
            raise InputError('Email already registered')

    # Check password is greater than 6 characters
    if len(password) < 6:
        raise InputError('Password too short')

    # Check name is within 1 and 50 characters
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError('First Name too long or short')

    # Check name is within 1 and 50 characters
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError('Last Name too long or short')

    # Create Handle
    handle = name_first + name_last
    if len(handle) > 20:  # keeping the handle under 20 chars
        handle = handle[0:20]

    # Creating a new dictionary for new user
    new_user = {
        'u_id': len(users),
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle,
        'token': create_token(email)
    }

    # Adding user to dictionary
    users.append(new_user)

    # Return new user id and token
    return {
        'u_id': new_user['u_id'],
        'token': new_user['token']
    }
