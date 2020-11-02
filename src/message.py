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
    
    # Get the selected channel
    channel = helper_functions.get_channel(token, channel_id)
    
    # Check if authorised user is a member of the channel    
    if not helper_functions.channel_member(token, channel):
        raise AccessError('Authorised user has not joined this channel yet')

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
    # Get the user that is sending the request
    authorised_user = helper_functions.get_authorised_user(token)

    # Get the channel where the message exists
    channel = helper_functions.get_channel_with_message(message_id)
    # Raise input error is channel cannot be found
    if channel is None:
        raise InputError("Message does not exist")

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
        raise AccessError("Message to remove was not sent by authorised user. Authorised user is not an owner of the channel")
    

def message_edit(token, message_id, message):
    '''
    Given a message, update it's text with new text. If the new message is an empty string, the message is deleted
    '''    
    
    # Get the user that is sending the request
    authorised_user = helper_functions.get_authorised_user(token)

    # Get the channel where the message exists
    channel = helper_functions.get_channel_with_message(message_id)
    
    # Raise input error is channel cannot be found
    if channel is None:
        raise InputError("Message does not exist")

    # Check if authorised user is channel owner or Flockr owner
    channel_owner = any((member['is_owner'] and member['u_id'] == authorised_user['u_id']) or (authorised_user['permission_id'] == 1 and member['u_id'] == authorised_user['u_id']) for member in channel['members'])
    
    # If the message is an empty message, delete the message
    if len(message) == 0:   
        channel['messages'].remove(message)
        return {}
    
    channel_message = helper_functions.get_message(message_id, channel)
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

    # Get the channel where the message is from a helper function
    channel = get_channel(token, message_id)

    # Throw error if no message, or user is not a member of that channel
    if channel == -1 or not channel_member(token, channel):
        raise InputError("Message_id is not a valid message within a channel that the authorised user has joined")
    
    # Get message from helper function
    message = get_message(message_id, channel)

    if message['react_id'] == 1:
        raise InputError("Message already contains an active react")
    
    # Update react and return
    message['react_id'] = 1
    update_message(message_id, message, channel)
    return {}


def message_unreact(token, message_id, react_id):
    '''
    Given a message with channel the authorised user is part of,
    remove "react" to that particular message
    '''
    # For now there are only two possible reacts
    if react_id != 1 or react_id != 0:
        raise InputError("React_id is not a valid React ID")

    # Get the channel where the message is from a helper function
    channel = get_channel(token, message_id)

    # Throw error if no message, or user is not a member of that channel
    if channel == -1 or not channel_member(token, channel):
        raise InputError("Message_id is not a valid message within a channel that the authorised user has joined")
    
    # Get message from helper function
    message = get_message(message_id, channel)

    if message['react_id'] == 0:
        raise InputError("Message already does not contain an active react")
    
    # Update react and return
    message['react_id'] = 0
    update_message(message_id, message, channel)
    return {}
    
def message_pin(token, message_id):
    '''
    Given a message within a channel, mark it as "pinned" to be given special
    display treatment by the frontend
    '''  

    # Get the channel where the message is from a helper function
    channel = get_channel(token, message_id)

    # Throw error if no message, or user is not a member of that channel
    if channel == -1:
        raise InputError("Message_id is not a valid message")
    
    # Throw error is user not member or owner of channel. By default an owner
    # is a member of the channel
    if not channel_member(token, channel):
        raise AccessError("The authorised user is not a member/owner of the channel")

    # Get message from helper function
    message = get_message(message_id, channel)

    if message['is_pinned']:
        raise InputError("Message is already pinned")
    
    # Update react and return
    message['is_pinned'] = True
    update_message(message_id, message, channel)
    return {}

def message_unpin(token, message_id):
    '''
    Given a message within a channel, mark it as unpinned
    '''  
    # Get the channel where the message is from a helper function
    channel = get_channel(token, message_id)

    # Throw error if no message, or user is not a member of that channel
    if channel == -1:
        raise InputError("Message_id is not a valid message")
    
    # Throw error is user not member or owner of channel. By default an owner
    # is a member of the channel
    if not channel_member(token, channel):
        raise AccessError("The authorised user is not a member/owner of the channel")

    # Get message from helper function
    message = get_message(message_id, channel)

    if not message['is_pinned']:
        raise InputError("Message is already unpinned")
    
    # Update react and return
    message['is_pinned'] = False
    update_message(message_id, message, channel)
    return {} 




