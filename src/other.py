from data import data, is_valid_token, load_token, get_user
import copy
from datetime import datetime
import calendar
from error import InputError, AccessError
import re


def clear():
    '''
    Resets the internal data of the application to it's initial state
    '''
    data['users'].clear()
    data['channels'].clear()

    return {}


def users_all(token):
    '''
    Returns a list of all users and their associated details
    '''
    return {
        'users': data['users'],
    }

def admin_userpermission_change(token, u_id, permission_id):
    '''
    Given a User by their user ID, set their permissions to new permissions described by permission_id
    '''
    users = data['users']
    
    # Validate permission_id is correct
    if permission_id < 1 or permission_id > 2:
        raise InputError('Permission_id does not refer to a value permission')
    
    # Check whether token is valid
    if is_valid_token(token) is not True:
        raise AccessError(description="Invalid token")
    
    # Get ui_d from jwt
    token_uid = load_token(token)['u_id']
    
    # Get the user that is sending the request
    authorised_user = get_user(token_uid)
    
    # Check authorised user permission is 1
    if authorised_user['permission_id'] != 1:
        raise InputError('The authorised user is not an admin or owner')

    # Get selected user 
    selected_user = next((user for user in users if user['u_id'] == u_id), None)

    # Check if u_id refers to valid user
    if selected_user is None:
        raise InputError('U_id does not refer to a valid user')

    # Set permission id
    selected_user['permission_id'] = permission_id

    return {}
 
def search(token, query_str):
    '''
    Given a query string, return a collection of messages in all of the channels
    that the user has joined that match the query
    '''
    all_messages = []

    channels = data['channels']

    # Check whether token is valid
    if is_valid_token(token) is not True:
        raise AccessError(description="Invalid token")
    
    # Get ui_d from jwt
    token_uid = load_token(token)['u_id']
    
    # Get the user that is sending the request
    authorised_user = get_user(token_uid)
    
    # Get each batch of messages from each channel where the user is a member
    for channel in channels:
        for member in channel['members']:
            if member['u_id'] == authorised_user['u_id']:
                all_messages += channel['messages']
                break
    
    # Get all the messages that match that 
    matched_messages = [message for message in all_messages if query_str in message['message']]

    return {
        'messages': matched_messages
    }

def get_timestamp():
    '''
    Returns a unix timestamp
    '''
    return datetime.now().timestamp()
 

def check(email):
    '''
    Checks that the entered email is valid based on regex expression
    '''
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    # Make a regular expression for validating an Email
    if re.search(regex, email):
        return True

    return False

