'''
import regex library
'''
import re
from flask import Flask, request
from data import data
from error import InputError

app = Flask(__name__)
def create_token(email):
    '''
    Creates a token for each user
    '''
    # creates a hash using in built python hash function
    return str(hash(email))


def check(email):
    '''
    Checks that the entered email is valid based on regex expression
    '''
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    # Make a regular expression for validating an Email
    if re.search(regex, email):
        return True

    return False

@app.route("/auth/login", methods=['POST'])
def auth_login():
    '''
    Login and authenticate existing user
    '''
    payload = request.get_json()
    email = payload['email']
    password = payload['password']

    # Check email is valid format
    if (check(email)) is not True:
        raise InputError('Invalid email')

    # Get users from data
    users = data['users']

    # Check that email and password are correct and valid
    user = next((user for user in users if user['email'] == email), None)

    # If the was not found based on email, throw exception
    if user is None:
        raise InputError('Incorrect email')

    # If password matches send back id and token
    # Else throw exception
    if user['password'] == password:
        return {
            'u_id': user['u_id'],
            'token': user['token']
        }

    raise InputError('Incorrect password')
@app.route("/auth/logout", methods=['POST'])
def auth_logout():
    '''
    Logout authenticated user
    '''
    payload = request.get_json()
    token = payload['token']
    # Get users from data
    users = data['users']

    # Check that token exists
    if any(user['token'] == token for user in users):
        return {'is_success': True}

    return {'is_success': False}

@app.route("/auth/register", methods=['POST'])
def auth_register():
    '''
    Register a new user
    '''
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    name_first = payload['name_first']
    name_last = payload['name_last']
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

    # Auto Increment the next user
    if len(users) == 0:
        new_user['u_id'] = 1
    else:
        new_user['u_id'] = users[-1]['u_id'] + 1

    # Adding user to dictionary
    users.append(new_user)

    # Return new user id and token
    return {
        'u_id': new_user['u_id'],
        'token': new_user['token']
    }
