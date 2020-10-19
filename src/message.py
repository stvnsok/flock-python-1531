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

    # Get the selected channel
    channel = next(channel for channel in data['channels'] if channel['channel_id'] == channel_id, None)

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
    
    messages = data['messages']
    channels = data['channels']
    
    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Get the channel where the message exists
    channel = next(channel for channel in channels for message in channel['messages'] if message['message_id'] == message_id)

    # Check if authorised user is owner
    channel_owner = any(member['permission_id'] == 1 and member['u_id'] == authorised_user['u_id'] for member in channel['members'])
    
    # Check the messages in the channel
    # Throw an access error if the message was not sent by authorised user, 
    # or authorised user is not an owner of the channel.
    for message in channel['messages']:
        if message['message_id'] == message_id:
            if message['u_id'] == authorised_user['u_id'] or channel_owner:
                channel['messages'].remove(message)
                return {}
            elif not channel_owner:
                raise AccessError("Authorised user is not an owner of the channel")
            else:
                raise AccessError("Message to remove was not sent by authorised user")
    

def message_edit(token, message_id, message):
    return {
    }