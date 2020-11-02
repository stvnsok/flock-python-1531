'''
Set of helper functions that help reduce code within actual features
themselves
'''

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



def get_channel(token, message_id):
    '''
    Get the channel where the given message is.
    '''    
    channels = data['channels']
    
    # Get the channel where the message exists
    channel = next((channel for channel in channels for message in channel['messages'] if message['message_id'] == message_id), None)

    # Raise input error is channel cannot be found
    if channel is None:
        return -1

    return channel

def channel_member(token, channel):
    '''
    See if a user is part of a channel
    '''
    authorised_user = next((user for user in data['users'] if user['token'] == token), None)

    return any(user['u_id'] == member['u_id'] for member in channel['members'])