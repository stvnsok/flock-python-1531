from data import data
import channel
from error import InputError, AccessError
import pytest
import re


def channels_list(token):
    '''
    channels_list
    Provide a list of all channels (and their associated details) that the authorised user is part of
    Parameters: (token)
    Return type: {channels}
    Exceptions: N/A
    '''

    # Get users from data
    users = data['users']
    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Check if user exists/ token is correct
    if authorised_user == None:
        # Need to fix this later
        raise AccessError('Token is incorrect/user does not exist')

    # Find all the channels where the authorised user is a member        
    channels = [channel for channel in data['channels'] for member in channel['members'] if authorised_user['u_id'] == member['u_id']];

    # Return channels
    return {'channels' : channels}


def channels_listall(token):
    '''
    channels_listall
    Provide a list of all channels (and their associated details)
    Parameters: (token)
    Return type: {channels}
    Exceptions: N/A
    '''

    # Get users from data
    users = data['users']
    
    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Check if user exists/ token is correct
    if authorised_user == None:
        # Need to fix this later
        raise AccessError('Token is incorrect/user does not exist')

    # Return channels
    return {'channels': data['channels']}


def channels_create(token, name, is_public):
    '''    
    channels_create
    Creates a new channel with that name that is either a public or private channel
    Parameters: (token, name, is_public)
    Return type: {channel_id}
    Exceptions: InputError when the name of the channel exceeds 20 characters
    '''

    # Get users from data
    users = data['users']
    channels = data['channels']

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Check if user exists/ token is correct
    if authorised_user == None:
        # Need to fix this later
        raise AccessError('Token is incorrect/user does not exist')

    # raise error for name being too long
    if len(name) > 20:
        raise InputError('Name too long')

    new_channel = {}

    # Method for assigning the channel id.
    # Will auto-increment from the last element u_id
    if len(channels) == 0:
        new_channel['channel_id'] = 1
    else:
        new_channel['channel_id'] = channels[-1]['channel_id'] + 1

    if is_public:
        new_channel['is_public'] = True
    else:
        new_channel['is_public'] = False

    # Add new channel to channels
    channels.append(new_channel)

    # Add creator of channel to channel
    channel.channel_addowner(
        token, new_channel['channel_id'], authorised_user['u_id'])

    # Return new channel
    return {'channel_id': new_channel['channel_id']}
