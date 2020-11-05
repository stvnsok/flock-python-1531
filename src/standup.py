'''
Standup.py
5/10/2020
'''
import threading
import time
from datetime import datetime, timedelta, timezone
from data import data
from message import message_send
from error import InputError, AccessError

def standup_start(token, channel_id, length):
    '''
    For a given channel, start the standup period whereby for the next "length"
    seconds if someone calls "standup_send" with a message, it is buffered during
    the X second window then at the end of the X second window a message will be
    added to the message queue in the channel from the user who started the standup.
    X is an integer that denotes the number of seconds that the standup occurs for.
    '''
    length = int(length)

    # Get users from data
    users = data['users']

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    #Check if user exists/ token is correct
    if authorised_user is None:
        raise AccessError('Token is incorrect')

    # Get channel from data
    channels = data['channels']

    # Finds the Channel, if it doesn't exists assigns None
    channel = next(
        (channel for channel in channels if channel['channel_id'] == channel_id), None)
    
    # Check if channel exists
    if channel is None:
        raise InputError('Channel_id does not exist')

    # Check if there is an active standup
    response = standup_active(token, channel_id)
    if response['is_active'] is True:
        raise InputError('An active standup is currently running in this channel')

    # Set is_active to true to start the standup
    channel['standup_active'] = True

    # Calulate the finish time of the startup
    time_finish = datetime.now() + timedelta(seconds=length)

    # Convert time_finish to unix timestamp
    unix_time_finish = time_finish.replace(tzinfo=timezone.utc).timestamp()

    # Add an standup key to channel database for buffered messages
    channel['standup'] = []

    # calls print_buffered_messages after length seconds
    t = threading.Timer(length, print_buffered_messages, [channel, channel_id, token])

    # continue without stopping for threading.Timer to finish
    t.start()

    return unix_time_finish

def print_buffered_messages(channel, channel_id, token):
    '''
    Joins up all the messages buffed in channel['standup'] with a '\n' between
    them. After it will pass this long string into messege_send function to be
    posted onto the channel. The buffed messages will be cleared after the string
    is sent.
    '''
    # join all messages in channel['standup'] list into a string
    buffered_messages = '\n'.join(channel['standup'])

    # send that string as a message
    message_send(token, channel_id, buffered_messages)

    # clears channel['standup'] list for furture standups
    messages_list = []

    # Set is_active to false
    channel['standup_active'] = False

def standup_active(token, channel_id):
    # Get users from data
    users = data['users']

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    #Check if user exists/ token is correct
    if authorised_user is None:
        raise AccessError('Token is incorrect')

    # Get channel from data
    channels = data['channels']

    # Finds the Channel, if it doesn't exists assigns None
    channel = next(
        (channel for channel in channels if channel['channel_id'] == channel_id), None)
    
    # Check if channel exists
    if channel is None:
        raise InputError('Channel_id does not exist')

    return {
        'is_active': False,
        'time_finish': None
    }

def standup_send(token, channel_id, message):

    '''
    Sending a message to get buffered in the standup queue, 
    assuming a standup is currently active
    '''
    # Get users from data
    users = data['users']

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    #Check if user exists/ token is correct
    if authorised_user is None:
        raise AccessError('Token is incorrect')

    # Get channel from data
    channels = data['channels']
    
    # Finds the Channel, if it doesn't exists assigns None
    channel = next(
        (channel for channel in channels if channel['channel_id'] == channel_id), None)
    
    # Check if channel exists
    if channel is None:
        raise InputError('Channel_id does not exist')
        
    # Check if there is an active standup
    response = standup_active(token, channel_id)
    if response['is_active'] is True:
    raise InputError('An active standup is currently running in this channel')
    
    #Check if authorised user is a member of the channel that the message is within
    if not any(authorised_user['u_id'] == member['u_id'] for member in channel['members']):
        raise AccessError('Authorised user is not a member of the channel')

    #standup = {authorised_user['u_id']: messages
    
    #channel['standup'].append(standup)
    
    # Note to steven, I except the following things from this function:
    # - messages send into here will be converted to the format of " 'handle': 'message' "
    #where the handle will the be user who called this function. 
    # - This formmated message will be passed into the channel['standup'] where
    #it will be appended to the end of the list within channel['standup']. 
    # (see the data.py for example)
    return {}
