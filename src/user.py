from data import data
from error import InputError, AccessError
from flask import request


def user_profile():

    token = request.args.get('token')
    u_id_str = request.args.get('u_id')
    u_id = int(u_id_str)
    # Get users from data
    users = data['users']

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

def user_profile_sethandle():

    payload = request.get_json()
    token = payload['token']
    handle_str = payload['handle_str']

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
    for curr_user in users:
        if curr_user['token'] == token:
            
    
    return {}

def user_profile_setname(token, name_first, name_last):
    
    payload = request.get_json()
    token = payload['token']
    handle_str = payload['handle_str']

    # Grabs all users from data
    users = data['users']
    
    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Check if user exists/ token is correct
    if authorised_user is None:
        raise AccessError('Token is incorrect')

    # Checking if length of first name is between 3 and 20 inclusive
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError("First name needs to be between 1 and 50")

    # Checking if length of last name is between 3 and 20 inclusive
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError("Last name needs to be between 1 and 50")

    # Update first name and last name of user
    authorised_user['name_first'] = name_first
    authorised_user['name_last'] = name_last

    return {}

def user_profile_setemail(token, email):
    return {
    }
