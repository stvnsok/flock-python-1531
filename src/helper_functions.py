'''
Set of helper functions that help reduce code within actual features
themselves
'''

from data import data

def get_authorised_user(token):
    '''
    Get an authorised user based on token
    '''
    return next((user for user in data['users'] if user['token'] == token), None)

def get_message(message_id, channel):
    '''
    Helper function that allows a message to be retrieved from a channel.
    Assumes message does exist and previous exceptions have been handled.
    '''
    
    for message in channel['messages']:
        if message['message_id'] == message_id:
            return message
    
    
def update_message(message_id, new_message, channel):
    '''
    Helper function to update a message quickly.
    Assumes message does exist and previous exceptions have been handled.
    '''

    for message in channel['messages']:
        if message['message_id'] == message_id:
            message = new_message
            return 

def get_channel(channel_id):
    '''
    Get the channel associated with the given channel_id
    '''
    
    return next((channel for channel in data['channels'] if channel['channel_id'] == channel_id), None)


def get_channel_with_message(message_id):
    '''
    Get the channel where the given message is.
    '''    
    
    return next((channel for channel in data['channels'] for message in channel['messages'] if message['message_id'] == message_id), None)


def channel_member(token, channel):
    '''
    See if a user is part of a channel
    '''
    
    user = next((user for user in data['users'] if user['token'] == token), None)

    return any(user['u_id'] == member['u_id'] for member in channel['members'])



