from data import *
from error import *


def channel_invite(token, channel_id, u_id):
    # Invites a user (with user id u_id) to join a channel with ID channel_id.
    # Once invited the user is added to the channel immediately

    channels = data['channels']
    users = data['users']

    # Finds the Channel, if it doesn't exists assigns None
    channel = next(
        (channel for channel in channels if channel['id'] == channel_id), None)

    # Finds the user, if it doesn't exists assigns None
    user = next((user for user in users if user['u_id'] == u_id), None)

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Check if channel exists
    if (channel == None):
        raise InputError('Channel_id does not exist')

    # Check if user exists
    if (user == None):
        raise InputError('U_id does not exist')

    # Check if authorised user is a member of the channel
    if not any(authorised_user['u_id'] == member['u_id'] for member in channel['all_members']):
        raise AccessError(
            'Authorised user is not a member of the channel')

    # User is added to channel's members
    new_member = {
        'u_id': user['u_id'],
        'name_first': user['name_first'],
        'name_last': user['name_last'],
    }
    channel['all_members'].append(new_member)

    return {}


def channel_details(token, channel_id):
    # Given a Channel with ID channel_id that the authorised user is part of,
    # provide basic details about the channel

    channels = data['channels']
    users = data['users']

    # Finds the Channel, if it doesn't exists assigns None
    channel = next(
        (channel for channel in channels if channel['id'] == channel_id), None)

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Check channel exists
    if (channel == None):
        raise InputError('Channel_id does not exist')

    # Check if authorised user is a member of the channel
    if not any(authorised_user['u_id'] == member['u_id'] for member in channel['all_members']):
        raise AccessError(
            'Authorised user is not a member of the channel')

    return {
        'name': channel['name'],
        'owner_members': channel['owner_members'],
        'all_members': channel['all_members'],
    }


def channel_messages(token, channel_id, start):

    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }


'''Given a Channel with ID channel_id that the authorised user is part of, 
return up to 50 messages between index "start" and "start + 50". Message with 
index 0 is the most recent message in the channel. This function returns a new 
index "end" which is the value of "start + 50", or, if this function has returned 
the least recent messages in the channel, returns -1 in "end" to indicate there are
no more messages to load after this return.'''


def channel_leave(token, channel_id):
    return {  # Given a channel ID, the user removed as a member of this channel
    }


def channel_join(token, channel_id):
    return {  # Given a channel_id of a channel that the authorised user can join,
        # adds them to that channel
    }


def channel_addowner(token, channel_id, u_id):
    return {  # Make user with user id u_id an owner of this channel
    }


def channel_removeowner(token, channel_id, u_id):
    return {  # Remove user with user id u_id an owner of this channel
    }
