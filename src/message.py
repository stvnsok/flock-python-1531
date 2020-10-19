from error import InputError, AccessError
from data import data
from other import get_timestamp
import uuid

def message_send(token, channel_id, message):

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

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
        'channel_id': channel_id
    }   

    # Add new message to dictionary
    data['messages'].append(new_message)

    return {
        'message_id': new_message['message_id'],
    }

def message_remove(token, message_id):
    
    messages = data['messages']
    channels = data['channels']
    
    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)
    
    # Get the mesage from messages
    message = next(message for message in messages if message['message_id'] == message_id, None);

    # If message does not exist throw error
    if message is None:
        raise InputError("Message does not exist")

    # Get the channel where this message exists    
    channel = next(channel for channel in channels if channel['channel_id'] = message['channel_id'])

    # Determine if authorised user is an owner of the channel where message was sent
    channel_owner = any(authorised_user['u_id'] == member['u_id'] and member['is_owner'] for member in channel['members'])

    # Throw error if not owner
    if not channel_owner:
        raise AccessError("Message to remove was not sent by an owner of this channel")

    # Throw error if the message was not sent by the authorised user 
    if not channel_owner and message['u_id'] != authorised_user['u_id']:
        raise AccessError("Message to remove was not sent by authorised user")
    
    # Remove message and return
    messages.remove(message)
    return {}
    

def message_edit(token, message_id, message):
    return {
    }