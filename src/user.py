from data import data
from error import InputError, AccessError
from other import check

def user_profile(token, u_id):

    # Get users from data
    users = data['users']

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    #Check if user exists/ token is correct
    if authorised_user is None:
        raise AccessError('Token is incorrect')

    # Searches for the user with the u_id
    users_checked = 0
    for user_id in users:
        if int(user_id['u_id']) == int(u_id):
            profile = user_id
        else:
            users_checked += 1

    # If list reaches end then raise error for no user found
    print(users_checked)
    print(len(users))
    if users_checked == len(users):
        raise InputError('No users with the entered u_id was found')
        
    return {
        'u_id': profile['u_id'],
        'email': profile['email'],
        'name_first': profile['name_first'],
        'name_last': profile['name_last'],
        'handle_str': profile['handle_str'],
    }

def user_profile_sethandle(token, handle_str):

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

    # Grabs all users from data
    users = data['users']

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Check if user exists/ token is correct
    if authorised_user is None:
        raise AccessError('Token is incorrect')

    # Raise errors for invalid name lengths
    if (len(name_first) > 50) or (len(name_first) < 1):
        raise InputError('First name must be between 1 and 50 characters in length')

    if (len(name_last) > 50) or (len(name_last) < 1):
        raise InputError('Last name must be between 1 and 50 characters in length')
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

    # Check email is valid format
    if check(email) is not True:
        raise InputError('Email is not valid')

    # Check if the email is already being used by another user
    if any(user['email'] == email and user['u_id'] != authorised_user['u_id'] for user in users):
       raise InputError("Email address is already in use")

    # Set email
    authorised_user['email'] = email
    return {}
