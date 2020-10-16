from data import data
from error import InputError, AccessError
from flask import request

def user_profile():

    token = request.args.get('token')
    u_id = request.args.get('u_id')

    # Get users from data
    users = data['users']

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Check if user exists/ token is correct
    if authorised_user is None:
        # Need to fix this later
        raise AccessError('Token is incorrect/user does not exist')

    # Searches for the user with the u_id
    for i, user_id in enumerate(users):
        if user_id['u_id'] == u_id:
            profile = user_id

    # If list reaches end then raise error for no user found
    if i == len(users):
        raise InputError('No users with the entered u_id was found')
        
    return {
        'u_id': profile['u_id'],
        'email': profile['email'],
        'name_first': profile['name_first'],
        'name_last': profile['name_last'],
        'handle_str': profile['handle_str'],
    }

def user_profile_sethandle():
    token = request.args.get('token')
    handle_str = request.args.get('handle_str')

    # checking if length of handle_str is between 3 and 20 inclusive
    if len(handle_str) <= 3 or len(handle_str) >= 20:
        raise InputError("Handle length needs to be between 3 and 2-")

    # Grabs all users from data
    users = data['users']
    
    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Check if user exists/ token is correct
    if authorised_user is None:
        # Need to fix this later
        raise AccessError('Token is incorrect/user does not exist')

    # Cycles through all users to check if given handle already exists
    for user_handle in users:
        if user_handle['handle_str'] == handle_str:
            raise InputError('Handle already in use by another user')

    # Update the handle_str of user
    for curr_user in users:
        if curr_user['token'] == token:
            curr_user['handle_str'] = handle_str
    
    return {}