from data import data
from error import InputError, AccessError
from flask import request
from other import check
import re 
  


def user_profile(token, u_id):

    # token = request.args.get('token')
    # u_id_str = request.args.get('u_id')
    # u_id = int(u_id_str)
    # Get users from data
    users = data['users']

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
    # Check if email uses valid syntax
    if not (re.search(regex, email)):
        raise InputError('Email entered is not a valid email')
    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    #Check if user exists/ token is correct
    if authorised_user is None:
        raise AccessError('Token is incorrect')

    # Searches for the user with the u_id
    usersChecked = 0
    for user_id in users:
        if user_id['u_id'] == u_id:
            profile = user_id
        else:
            usersChecked += 1

    # If list reaches end then raise error for no user found
    print(usersChecked)
    if usersChecked == len(users):
        raise InputError('No users with the entered u_id was found')
        
    return {
        'u_id': profile['u_id'],
        'email': profile['email'],
        'name_first': profile['name_first'],
        'name_last': profile['name_last'],
        'handle_str': profile['handle_str'],
    }

def user_profile_sethandle(token, handle_str):

    # payload = request.get_json()
    # token = payload['token']
    # handle_str = payload['handle_str']

    # Grabs all users from data
    users = data['users']
    
    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Check if user exists/ token is correct
    if authorised_user is None:
        raise AccessError('Token is incorrect')

    # checking if length of handle_str is between 3 and 20 inclusive
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError("Handle length needs to be between 3 and 20")
    
    # Cycles through all users to check if given handle already exists
    for user_handle in users:
        if user_handle['handle_str'] == handle_str:
            raise InputError('Handle already in use by another user')
    
    
    # Update the handle_str of user
    authorised_user['handle_str'] = handle_str
            
    return {}

def user_profile_setname(token, name_first, name_last):
    # Get input from json and store in variables 
    # payload = request.get_json()
    # token = payload['token']
    # first = payload['name_first']
    # last = payload['name_last']

    # Grabs all users from data
    users = data['users']
    
    # Check if user exists/ token is correct
    if authorised_user is None:
        raise AccessError('Token is incorrect')

    # Raise errors for invalid name lengths
    if (len(first) > 50) or (len(first) < 1):
         raise InputError('First name must be between 1 and 50 characters in length')

    if (len(second) > 50) or (len(second) < 1):
         raise InputError('Second name must be between 1 and 50 characters in length')   

    # Update first name and last name of user
    authorised_user['name_first'] = name_first
    authorised_user['name_last'] = name_last

    return {}

def user_profile_setemail(token, email):
    # Grabs all users from data
    users = data['users']
    
    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Check if user exists/ token is correct
    if authorised_user is None:
        raise AccessError('Token is incorrect')

    # Check if email is valid
    if not (re.search(regex, email)):
        raise InputError('Email is not valid')
    
    # Check if the email is already being used by another user
    if any(user['email'] == email and user['u_id'] != authorised_user['u_id'] for user in users):
        raise InputError("Email address is already in use")

    # Set email    
    authorised_user['email'] = email
    return {}
