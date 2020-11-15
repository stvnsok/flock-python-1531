'''
Auth function
'''
import smtplib
from flask import request
from error import InputError
from other import check, clear
from data import (data, check, create_token, hash_password, is_valid_token)

#@APP.route("/auth/login", methods=['POST'])
def auth_login(email, password):
    '''
    Login and authenticate existing user
    '''
    # Check email is valid format
    if (check(email)) is not True:
        raise InputError('Invalid email')

    # Get users from data
    users = data['users']

    # Check that email and password are correct and valid
    user = next((user for user in users if user['email'] == email), None)

    # If the was not found based on email, throw exception
    if user is None:
        raise InputError('Email does not belong to a user')

    # If password matches send back id and token
    # Else throw exception
    if user['password'] == hash_password(password):
        return {
            'u_id': user['u_id'],
            'token': create_token(user['u_id'])
        }

    raise InputError('Incorrect password')
#@APP.route("/auth/logout", methods=['POST'])
def auth_logout(token):
    '''
    Logout authenticated user
    '''

    # Check that token exists
    if is_valid_token(token):
        data['invalid_tokens'].append(token)
        return {'is_success': True}
    # if any(user['token'] == token for user in users):
    #     return {'is_success': True}

    return {'is_success': False}

#@APP.route("/auth/register", methods=['POST'])
def auth_register(email, password, name_first, name_last):
    '''
    Register a new user
    '''
    # Check email is valid format
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

    # Hash the password
    password = hash_password(password)
    
    # Creating a new dictionary for new user
    new_user = {
        'u_id': len(users),
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last,
        'handle_str': handle,
        'permission_id' : 1 if len(users) == 0 else 2,
        'profile_img_url': '',
        'reset': None,
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
        'token': create_token(new_user['u_id'])
    }


#@APP.route("/auth/passwordreset/request", methods=['POST'])
def auth_passwordreset_request(email):
    # Get users from data
    users = data['users']

    # Check that email is valid
    user = next((user for user in users if user['email'] == email), None)

    if user is not None:
        encoded = user['password']

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        email_address = "noreplyflockr@gmail.com"
        email_password = "Hatsunemiku"

        server.login(email_address, email_password)

        user_name = user['name_first'] + ' ' + user['name_last'] 

        message_subject = "Your Flockr password reset request"
        message_body = "Hello" + ' ' + user_name + ' ' + "your password reset code is:"

        message = f'Subject: {message_subject}\n\n{message_body}\n\n{encoded}'
        server.sendmail('noreplyflockr@gmail.com', email, message)
        server.close()

    return {}

#@APP.route("/auth/passwordreset/reset, methods=['POST'])
def auth_passwordreset_reset(reset_code, new_password):   
    users = data['users']
    user = user = next((user for user in users if user['password'] == reset_code), None)

    if user is None:
        raise InputError('Invalid reset code')

    # Check password is greater than 6 characters
    if len(new_password) < 6:
        raise InputError('Password too short')
              
    user['password'] = hash_password(new_password)
  
    return {}
