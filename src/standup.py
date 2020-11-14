'''
Standup.py
5/10/2020
'''
import threading
import time
from datetime import datetime, timedelta, timezone
from data import data
from message import message_send, message_sendlater
from error import InputError, AccessError
from data import (
                    data, get_channel, channel_member, get_all_messages, 
                    get_authorised_user, get_channel_with_message, 
                    update_message, get_message, get_user, is_valid_token,
                    load_token)

def standup_start(token, channel_id, length):
    '''
    For a given channel, start the standup period whereby for the next "length"
    seconds if someone calls "standup_send" with a message, it is buffered during
    the X second window then at the end of the X second window a message will be
    added to the message queue in the channel from the user who started the standup.
    X is an integer that denotes the number of seconds that the standup occurs for.
    '''
    length = int(length)

    if is_valid_token(token) is not True:
        raise AccessError(description="Invalid token")

    # Finds the Channel, if it doesn't exists assigns None
    channel = get_channel(channel_id)
    
    # Check if channel exists
    if channel is None:
        raise InputError('Channel_id does not exist')

    # Check if there is an active standup
    response = standup_active(token, channel_id)
    if response['is_active'] is True:
        raise InputError('An active standup is currently running in this channel')

    # Calulate the finish time of the startup
    time_finish = datetime.now() + timedelta(seconds=length)

    # Convert time_finish to unix timestamp
    unix_time_finish = time_finish.replace(tzinfo=timezone.utc).timestamp()

    # Add an standup key to channel database for buffered messages
    channel['standup'] = {
        'is_active' : True,
        'time_finish' : unix_time_finish
    }

    return {'time_finish' : unix_time_finish}

# def print_buffered_messages(channel, channel_id, token):
#     '''
#     Joins up all the messages buffed in channel['standup'] with a '\n' between
#     them. After it will pass this long string into messege_send function to be
#     posted onto the channel. The buffed messages will be cleared after the string
#     is sent.
#     '''
#     # # join all messages in channel['standup'] list into a string
#     # buffered_messages = '\n'.join(channel['standup']['queue'])

#     # # send that string as a message
#     # message_send(token, channel_id, buffered_messages)

#     for message in channel['standup']['queue']:
#         message_send(token, channel_id, message)

#     # clears channel['standup'] list for furture standups
#     channel['standup']['queue'] = []
#     # Set is_active to false
#     channel['standup']['is_active'] = False

def standup_active(token, channel_id):
    '''
    For a given channel, return whether a standup is active in it, 
    and what time the standup finishes. If no standup is active,
    then time_finish returns None
    '''
    if is_valid_token(token) is not True:
        raise AccessError(description="Invalid token")
    
    
    # Finds the Channel, if it doesn't exists assigns None
    channel = get_channel(channel_id)
    
    # Check if channel exists
    if channel is None:
        raise InputError('Channel_id does not exist')

    if channel['standup']['is_active']:
        return {
            'is_active': channel['standup']['is_active'],
            'time_finish': channel['standup']['time_finish']
        }    
    
    return {
        'is_active': False,
        'time_finish': None
    }

def standup_send(token, channel_id, message):

    '''
    Sending a message to get buffered in the standup queue, 
    assuming a standup is currently active
    '''
    
    # - messages send into here will be converted to the format of " 'handle': 'message' "
    #where the handle will the be user who called this function. 
    # - This formmated message will be passed into the channel['standup'] where
    #it will be appended to the end of the list within channel['standup']. 
    

    if is_valid_token(token) is not True:
        raise AccessError(description="Invalid token")
    
    # Get ui_d from jwt
    token_uid = load_token(token)['u_id']
    
    # Get the user that is sending the request
    authorised_user = get_user(token_uid)
    
    # Finds the Channel, if it doesn't exists assigns None
    channel = get_channel(channel_id)
    
    # Check if channel exists
    if channel is None:
        raise InputError('Channel_id does not exist')
        
    # Check if there is no active standup
    response = standup_active(token, channel_id)
    if response['is_active'] is False:
        raise InputError('An active standup is currently not running in this channel')
    
    #Check if authorised user is a member of the channel that the message is within
    if not channel_member(authorised_user, channel):
        raise AccessError('Authorised user is not a member of the channel')

    # Check if message is more than 1000 characters 
    if len(message) > 1000:   
        raise InputError('Message is more than 1000 characters')
    
    # get the standup    
    standup_message = authorised_user['handle_str'] + ' : ' + message
    # standup = authorised_used['handle_str'] + ':' message 
    # send message into queue
    message_sendlater(token, channel['channel_id'], standup_message, response['time_finish'])
    # # Append the message to the end of list
    # channel['standup']['queue'].append(standup)

    return {}
