from error import InputError, AccessError
from data import data
from other import get_timestamp
import uuid
import helper_functions 


def message_send(token, channel_id, message):
    '''
    Send a message from the authorised_user to the channel specified by channel_id 
    '''

    # Get the user that is sending the request
    authorised_user = helper_functions.get_authorised_user(token)

    if authorised_user is None:
        raise AccessError(description="Invalid token")
    
    # Get the selected channel
    channel = helper_functions.get_channel(channel_id)
    
    # Check if authorised user is a member of the channel    
    if not helper_functions.channel_member(token, channel):
        raise AccessError(description="Authorised user has not joined this channel yet")

    # Check if message is too long
    if len(message) > 1000:
        raise InputError(description="Message is more than 1000 characters")
    
    # Create new message object
    new_message = {
        'message_id' : 0,
        'message' : message,
        'u_id': authorised_user['u_id'],
        'time_created': get_timestamp(),
        'reacts': [],
        'is_pinned': False
    }   
    
    all_messages = helper_functions.get_all_messages()

    if len(all_messages) == 0:
        new_message['message_id'] = 0
    else:
        new_message['message_id'] = all_messages[-1]['message_id'] + 1

    # Add new message to dictionary
    channel['messages'].append(new_message)

    return {
        'message_id': new_message['message_id'],
    }

def message_remove(token, message_id):
    '''
    Given a message_id for a message, this message is removed from the channel
    '''
    # Get the user that is sending the request
    authorised_user = helper_functions.get_authorised_user(token)

    if authorised_user is None:
        raise AccessError(description="Invalid token")

    # Get the channel where the message exists
    channel = helper_functions.get_channel_with_message(message_id)
    # Raise input error is channel cannot be found
    if channel is None:
        raise InputError(description="Message does not exist")

    # Check if authorised user is channel owner or Flockr owner
    channel_owner = any((member['is_owner'] and member['u_id'] == authorised_user['u_id']) or (authorised_user['permission_id'] == 1 and member['u_id'] == authorised_user['u_id']) for member in channel['members'])
    
    # Check the messages in the channel
    # Throw an access error if the message was not sent by authorised user, 
    # or authorised user is not an owner of the channel.
    message = helper_functions.get_message(message_id, channel)
    if message['u_id'] == authorised_user['u_id'] or channel_owner:
        channel['messages'].remove(message)
        return {}
    else:
        raise AccessError(description="Message to remove was not sent by authorised user. Authorised user is not an owner of the channel")
    

def message_edit(token, message_id, message):
    '''
    Given a message, update it's text with new text. If the new message is an empty string, the message is deleted
    '''    
    
    # Get the user that is sending the request
    authorised_user = helper_functions.get_authorised_user(token)

    if authorised_user is None:
        raise AccessError(description="Invalid token")

    # Get the channel where the message exists
    channel = helper_functions.get_channel_with_message(message_id)
    
    # Raise input error is channel cannot be found
    if channel is None:
        raise InputError(description="Message does not exist")

    # Check if authorised user is channel owner or Flockr owner
    channel_owner = any((member['is_owner'] and member['u_id'] == authorised_user['u_id']) or (authorised_user['permission_id'] == 1 and member['u_id'] == authorised_user['u_id']) for member in channel['members'])
    
    # If the message is an empty message, delete the message
    if len(message) == 0:   
        message_to_remove = helper_functions.get_message(message_id, channel)
        channel['messages'].remove(message_to_remove)
        return {}
    
    channel_message = helper_functions.get_message(message_id, channel)
    if channel_message['u_id'] == authorised_user['u_id'] or channel_owner:
        channel_message['message'] = message
        return {}
    else:
        raise AccessError(description="Message to remove was not sent by authorised user. Authorised user is not an owner of the channel")

def message_sendlater(token, channel_id, message, time_sent):
    '''
    Send a message by an authenticated user to the channel with channel_id at 
    a specified time 
    '''
    # Get the user that is sending the request
    authorised_user = helper_functions.get_authorised_user(token)

    if authorised_user is None:
        raise AccessError(description="Invalid token")

    channel = helper_functions.get_channel(channel_id)

    if channel is None:
        raise InputError(description="Invalid channel")

    time_now = get_timestamp()

    if time_sent < time_now:
        raise InputError(description="Time sent is a time in the past")

    if len(message) > 1000:
        raise InputError(description="Message is more than 1000 characters")

    if not helper_functions.channel_member(token, channel):
        raise AccessError(description="Authorised user has not joined the channel")

    # Create new message object
    new_message = {
        'message_id' : 0,
        'message' : message,
        'u_id': authorised_user['u_id'],
        'time_created': time_now,
        'reacts': [],
        'is_pinned': False
    }   
    
    all_messages = helper_functions.get_all_messages()
    
    if len(all_messages) == 0:
        new_message['message_id'] = 0
    else:
        new_message['message_id'] = all_messages[-1]['message_id'] + 1

    # Add new message to dictionary
    channel['messages'].append(new_message)

    return {
        'message_id': new_message['message_id'],
    }
    
def message_react(token, message_id, react_id):
    '''
    Given a message with channel the authorised user is part of,
    add a "react" to that particular message
    '''
    
    # Get the user that is sending the request
    authorised_user = helper_functions.get_authorised_user(token)

    if authorised_user is None:
        raise AccessError(description="Invalid token")

    reacts = [0,1]
    # For now there are only two possible reacts
    if react_id not in reacts:
        raise InputError(description="React_id is not a valid React ID")

    authorised_user = helper_functions.get_authorised_user(token)

    # Get the channel where the message is from a helper function
    channel = helper_functions.get_channel_with_message(message_id)

    # Throw error if no message, or user is not a member of that channel
    if channel is None or not helper_functions.channel_member(token, channel):
        raise InputError(description="Message_id is not a valid message within a channel that the authorised user has joined")
    
    # Get message from helper function
    message = helper_functions.get_message(message_id, channel)

    react = None

    if len(message['reacts']) > 0:
        react = next((react for react in message['reacts'] if react['u_id'] == authorised_user['u_id']), None)

    # Create new react
    if react is None:
        new_react = {
            'u_id' : authorised_user['u_id'],
            'react_id' : [react_id]
        }
        message['reacts'].append(new_react)
        helper_functions.update_message(message_id, message, channel)
        return {}

    # Check if the react is already active
    if react_id in react['react_id']:
        raise InputError(description="Message already contains an active react with react_id")

    # Update react 
    react['react_id'].append(react_id)
    helper_functions.update_message(message_id, message, channel)
    return {}
    
    

def message_unreact(token, message_id, react_id):
    '''
    Given a message with channel the authorised user is part of,
    remove "react" to that particular message
    '''
    
    # Get the user that is sending the request
    authorised_user = helper_functions.get_authorised_user(token)

    if authorised_user is None:
        raise AccessError(description="Invalid token")    
    
    reacts = [0,1]
    # For now there are only two possible reacts
    if react_id not in reacts:
        raise InputError(description="React_id is not a valid React ID")

    authorised_user = helper_functions.get_authorised_user(token)
    # Get the channel where the message is from a helper function
    channel = helper_functions.get_channel_with_message(message_id)

    # Throw error if no message, or user is not a member of that channel
    if channel is None or not helper_functions.channel_member(token, channel):
        raise InputError(description="Message_id is not a valid message within a channel that the authorised user has joined")
    
    # Get message from helper function
    message = helper_functions.get_message(message_id, channel)

    react = None

    if len(message['reacts']) > 0:
        react = next((react for react in message['reacts'] if react['u_id'] == authorised_user['u_id']), None)

    # Cannot react to something that has no react
    if react is None or react_id not in react['react_id']:
        raise InputError(description="Message already does not contain an active react with react_id")
    

    # Update react
    react['react_id'].remove(react_id)
    helper_functions.update_message(message_id, message, channel)
    return {}
    
    
def message_pin(token, message_id):
    '''
    Given a message within a channel, mark it as "pinned" to be given special
    display treatment by the frontend
    '''  

    # Get the user that is sending the request
    authorised_user = helper_functions.get_authorised_user(token)

    if authorised_user is None:
        raise AccessError(description="Invalid token")

    # Get the channel where the message is from a helper function
    channel = helper_functions.get_channel_with_message(message_id)

    # Throw error if no message, or user is not a member of that channel
    if channel is None:
        raise InputError(description="Message_id is not a valid message")
    
    # Throw error is user not member or owner of channel. By default an owner
    # is a member of the channel
    if not helper_functions.channel_member(token, channel):
        raise AccessError(description="The authorised user is not a member/owner of the channel")

    # Get message from helper function
    message = helper_functions.get_message(message_id, channel)

    if message['is_pinned']:
        raise InputError("Message is already pinned")
    
    # Update react and return
    message['is_pinned'] = True
    helper_functions.update_message(message_id, message, channel)
    return {}

def message_unpin(token, message_id):
    '''
    Given a message within a channel, mark it as unpinned
    '''  

    # Get the user that is sending the request
    authorised_user = helper_functions.get_authorised_user(token)

    if authorised_user is None:
        raise AccessError(description="Invalid token")

    # Get the channel where the message is from a helper function
    channel = helper_functions.get_channel_with_message(message_id)

    # Throw error if no message, or user is not a member of that channel
    if channel is None:
        raise InputError(description="Message_id is not a valid message")
    
    # Throw error is user not member or owner of channel. By default an owner
    # is a member of the channel
    if not helper_functions.channel_member(token, channel):
        raise AccessError(description="The authorised user is not a member/owner of the channel")

    # Get message from helper function
    message = helper_functions.get_message(message_id, channel)

    if not message['is_pinned']:
        raise InputError(description="Message is already unpinned")
    
    # Update react and return
    message['is_pinned'] = False
    helper_functions.update_message(message_id, message, channel)
    return {} 

