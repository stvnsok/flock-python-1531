from data import data
import re
import pytest
from error import InputError
from channel import channel_addowner

def channels_list(token):
    # Get users from data
    users = data['users']

    # Check that token exists
    valid_token = 0
    for user in users:
        if (user['token'] == token):
            valid_token = 1
            break
    
    # raise error for invalid token
    if valid_token == 0 and len(users) is not 0:
        raise InputError('invalid token')
        
    #to do: finish channels list
    #phillip says hi to steven
    #steven says hi
    

def channels_listall(token):
    # Get users from data
    users = data['users']

    # Check that token exists
    valid_token = 0
    for user in users:
        if (user['token'] == token):
            valid_token = 1
            break
    
    # raise error for invalid token
    if valid_token == 0 and len(users) is not 0:
        raise InputError('invalid token or no registered users')

    return data['channels']

def channels_create(token, name, is_public):
    # Get users from data
    users = data['users']

    # Check that token exists
    valid_token = 0
    for user in users:
        if (user['token'] == token):
            valid_token = 1
            break
    
    # raise error for invalid token
    if valid_token == 0 and len(users) is not 0:
        raise InputError('invalid token')
    
    # raise error for name being too long
    if len(name) > 20:
        raise InputError('Name too long')

    # Grabs all channels from data
    channels = data['channels']

    # Generate channel id based on the number of exisiting channels
    channel_id = 0
    for channel in channels:
        channel_id += 1

    # Creating a new dictornary for new channel
    new_channel = {
        'channel_id': channel_id,
        'name': name,
        'is_public': is_public,
    }

    # Adding channel to dictionary
    channels.append(new_channel)

    # Adding the whoever called this function as the owner of the channel
    for user in users:
        if (user['token'] == token):
            channel_addowner(token, channel_id, user['u_id'])
            break

    return {
        'channel_id': new_channel['channel_id'],
        'name': new_channel['name'],
    }

