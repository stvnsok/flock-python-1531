from error import InputError, AccessError
from data import data
from other import get_timestamp
import uuid
from auth import *
from channels import *
from other import *


def find_message(token, message_id):
    '''
    Find a message for a given id. If it can't be found return -1
    '''
    channels = data['channels']

    authorised_user = next((user for user in users if user['token'] == token), None)

    # Get each batch of messages from each channel where the user is a member
    for channel in channels:
        for member in channel['members']:
            if member['u_id'] == authorised_user['u_id']:
                for message in channel['messages']:
                    if message['message_id'] == message_id:
                        return message

    # Not found so return -1
    return -1

def message_send(token, channel_id, message):
    '''
    Send a message from the authorised_user to the channel specified by channel_id 
    '''

    users = data['users']
    channels = data['channels']

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)
    
    # Get the selected channel
    channel = next((channel for channel in channels if channel['channel_id'] == channel_id), None)

    # Check if authorised user is a member of the channel
    if not any(authorised_user['u_id'] == member['u_id'] for member in channel['members']):
        raise AccessError(
            'Authorised user has not joined this channel yet')    
    
    # Check if message is too long
    if len(message) > 1000:
        raise InputError("Message is more than 1000 characters")

    # Create new message object
    new_message = {
        'message_id' : str(uuid.uuid4()),
        'message' : message,
        'u_id': authorised_user['u_id'],
        'time_created': get_timestamp()
    }   

    # Add new message to dictionary
    channel['messages'].append(new_message)

    return {
        'message_id': new_message['message_id'],
    }

def message_remove(token, message_id):
    '''
    Given a message_id for a message, this message is removed from the channel
    '''
    users = data['users']
    channels = data['channels']
    
    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Get the channel where the message exists
    channel = next((channel for channel in channels for message in channel['messages'] if message['message_id'] == message_id), None)

    # Raise input error is channel cannot be found
    if channel is None:
        raise InputError("Message does not exist")

    # Check if authorised user is channel owner or Flockr owner
    channel_owner = any((member['is_owner'] and member['u_id'] == authorised_user['u_id']) or (authorised_user['permission_id'] == 1 and member['u_id'] == authorised_user['u_id']) for member in channel['members'])

    # Check the messages in the channel
    # Throw an access error if the message was not sent by authorised user, 
    # or authorised user is not an owner of the channel.
    for message in channel['messages']:
        if message['message_id'] == message_id:
            if message['u_id'] == authorised_user['u_id'] or channel_owner:
                channel['messages'].remove(message)
                return {}
            else:
                raise AccessError("Message to remove was not sent by authorised user. Authorised user is not an owner of the channel")
    

def message_edit(token, message_id, message):
    '''
    Given a message, update it's text with new text. If the new message is an empty string, the message is deleted
    '''    
    users = data['users']
    channels = data['channels']
    
    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Get the channel where the message exists
    channel = next((channel for channel in channels for message in channel['messages'] if message['message_id'] == message_id), None)

    # Raise input error is channel cannot be found
    if channel is None:
        raise InputError("Message does not exist")

    # Check if authorised user is channel owner or Flockr owner
    channel_owner = any((member['is_owner'] and member['u_id'] == authorised_user['u_id']) or (authorised_user['permission_id'] == 1 and member['u_id'] == authorised_user['u_id']) for member in channel['members'])
    
    # If the message is an empty message, delete the message
    if len(message) == 0:   
        channel['messages'].remove(message)
        return {}
    
    for channel_message in channel['messages']:
        if channel_message['message_id'] == message_id:
            if channel_message['u_id'] == authorised_user['u_id'] or channel_owner:
                channel_message['message'] = message
                return {}
            else:
                raise AccessError("Message to remove was not sent by authorised user. Authorised user is not an owner of the channel")


def message_react(token, message_id, react_id):
    '''
    Given a message with channel the authorised user is part of,
    add a "react" to that particular message
    '''
    # For now there are only two possible reacts
    if react_id != 1 or react_id != 0:
        raise InputError("React_id is not a valid React ID")

    users = data['users']
    channels = data['channels']

    # Verify authorised user
    authorised_user = next((user for user in users if user['token'] == token), None)
    
    # Get each batch of messages from each channel where the user is a member
    for channel in channels:
        for member in channel['members']:
            if member['u_id'] == authorised_user['u_id']:
                for message in channel['messages']:
                    if message['message_id'] == message_id:
                        if message['react_id'] == 1:
                            raise InputError("Message already contains an active react")
                        else:
                            message['react_id'] = 1
                            return {}
    
    raise InputError("Message_id is not a valid message within a channel that the authorised user has joined")

def message_unreact(token, message_id, react_id):
    '''
    Given a message with channel the authorised user is part of,
    remove "react" to that particular message
    '''
    # For now there are only two possible reacts
    if react_id != 1 or react_id != 0:
        raise InputError("React_id is not a valid React ID")

    users = data['users']
    channels = data['channels']

    # Verify authorised user
    authorised_user = next((user for user in users if user['token'] == token), None)
    
    # Get each batch of messages from each channel where the user is a member
    for channel in channels:
        for member in channel['members']:
            if member['u_id'] == authorised_user['u_id']:
                for message in channel['messages']:
                    if message['message_id'] == message_id:
                        if message['react_id'] == 0:
                            raise InputError("Message does not already contains an active react")
                        else:
                            message['react_id'] = 0
                            return {}
    
    raise InputError("Message_id is not a valid message within a channel that the authorised user has joined")

    



