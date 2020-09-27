from data import *
import re
import pytest
from error import InputError

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
        raise InputError('invalid token')

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

    # Counting the number of private and public channels
    private_channel_count = 0
    public_channel_count = 0
    for channel in channels:
        if channel['channel_id'] >= 9000 and  channel['channel_id'] < 10000:
            private_channel_count += 1
        elif channel['channel_id'] >= 1000 and channel['channel_id'] < 2000:
            public_channel_count += 1
    # Generate channel id
    if is_public is True:
        channel_id = 1000 + public_channel_count
    else:
        channel_id = 9000 + private_channel_count

    # Creating a new dictornary for new channel
    new_channel = {
        'channel_id': channel_id,
        'name': name,
    }

    # Adding user to dictionary
    channels.append(new_channel)

    return {
        'channel_id': new_channel['channel_id'],
        'name': new_channel['name'],
    }
