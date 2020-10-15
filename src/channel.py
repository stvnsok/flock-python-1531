'''
import data dictionary from data.py
'''
from data import data
from error import InputError, AccessError


def channel_invite(token, channel_id, u_id):
    '''
    Invites a user (with user id u_id) to join a channel with ID channel_id.
    Once invited the user is added to the channel immediately
    '''

    channels = data['channels']
    users = data['users']

    # Finds the Channel, if it doesn't exists assigns None
    channel = next(
        (channel for channel in channels if channel['channel_id'] == channel_id), None)

    # Finds the user, if it doesn't exists assigns None
    user = next((user for user in users if user['u_id'] == u_id), None)

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Check if channel exists
    if channel is None:
        raise InputError('Channel_id does not exist')

    # Check if user exists
    if user is None:
        raise InputError('U_id does not exist')

    # Check if authorised user is a member of the channel
    if not any(authorised_user['u_id'] == member['u_id'] for member in channel['members']):
        raise AccessError(
            'Authorised user is not a member of the channel')

    # User is added to channel's members
    new_member = {
        'u_id': user['u_id'],
        'name_first': user['name_first'],
        'name_last': user['name_last'],
        'is_owner': False
    }

    channel['members'].append(new_member)
    return {}


def channel_details(token, channel_id):
    '''
    Given a Channel with ID channel_id that the authorised user is part of,
    provide basic details about the channel
    '''

    channels = data['channels']
    users = data['users']

    # Finds the Channel, if it doesn't exists assigns None
    channel = next(
        (channel for channel in channels if channel['channel_id'] == channel_id), None)

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Check channel exists
    if channel is None:
        raise InputError('Channel_id does not exist')

    # Check if authorised user is a member of the channel
    if not any(authorised_user['u_id'] == member['u_id'] for member in channel['members']):
        raise AccessError(
            'Authorised user is not a member of the channel')

    # Get all the owner members of the channel
    owner_members = [
        member for member in channel['members'] if member['is_owner']]

    return {
        'name': channel['name'],
        'owner_members': owner_members,
        'all_members': channel['members'],
    }


def channel_messages(token, channel_id, start):
    '''
    Given a Channel with ID channel_id that the authorised user is part of,
    return up to 50 messages between index "start" and "start + 50". Message with
    index 0 is the most recent message in the channel. This function returns a new
    index "end" which is the value of "start + 50", or, if this function has returned
    the least recent messages in the channel, returns -1 in "end" to indicate there are
    no more messages to load after this return.
    '''

    channels = data['channels']
    users = data['users']
    messages = data['messages']

    # Finds the Channel, if it doesn't exists assigns None
    channel = next(
        (channel for channel in channels if channel['channel_id'] == channel_id), None)

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Check if channel exists
    if channel is None:
        raise InputError('Channel_id does not exist')

    # Check if authorised user is a member of the channel
    if not any(authorised_user['u_id'] == member['u_id'] for member in channel['members']):
        raise AccessError(
            'Authorised user is not a member of the channel')

    # Gets all the messages for the given channel
    messages_from_channel = [
        message for message in messages if message['channel_id'] == channel['channel_id']]

    # sets the index for the last message
    end = start + 50

    if len(messages_from_channel) < start:
        raise InputError('Start is greater than total number of messages')

    # if this index is greater than the amount of messages then
    # the amount of remaining messages after the start index
    # is less than 50
    if len(messages_from_channel) < end:
        end = -1
        messages_from_channel = messages_from_channel[start:]
    # send back messages between the start and end range
    else:
        messages_from_channel = messages_from_channel[start: end]

    # return result
    return {
        'messages': messages_from_channel,
        'start': start,
        'end': end,
    }


def channel_leave(token, channel_id):
    '''
    Given a channel ID, the user removed as a member of this channel
    '''

    channels = data['channels']
    users = data['users']

    # Finds the Channel, if it doesn't exists assigns None
    channel = next(
        (channel for channel in channels if channel['channel_id'] == channel_id), None)

    # Check if channel exists
    if channel is None:
        raise InputError('Channel_id does not exist')

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Find the authorised user from the channel
    user = next((member for member in channel['members']
                 if authorised_user['u_id'] == member['u_id']), None)

    # Check if authorised user is a member of the channel
    if user is None:
        raise AccessError(
            'Authorised user is not a member of the channel')

    # If member remove them from channel
    channel['members'] = [member for member in channel['members']
                          if member['u_id'] != user['u_id']]

    return {}


def channel_join(token, channel_id):
    '''
    Given a channel_id of a channel that the authorised user can join,
    adds them to that channel
    '''

    channels = data['channels']
    users = data['users']

    # Finds the Channel, if it doesn't exists assigns None
    channel = next(
        (channel for channel in channels if channel['channel_id'] == channel_id), None)

    # Check if channel exists
    if channel is None:
        raise InputError('Channel_id does not exist')

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Determine whether channel is public or private
    # If channel is public, add them to the channel
    # Otherwise throw an exception
    if channel['is_public']:
        member = {
            'u_id': authorised_user['u_id'],
            'name_first': authorised_user['name_first'],
            'name_last': authorised_user['name_last'],
            'is_owner': False
        }
        channel['members'].append(member)
    else:
        raise AccessError(
            'Channel_id refers to a channel that is private')

    return {}


def channel_addowner(token, channel_id, u_id):
    '''
    Make user with user id u_id an owner of this channel
    '''

    channels = data['channels']
    users = data['users']

    # Finds the Channel, if it doesn't exists assigns None
    channel = next(
        (channel for channel in channels if channel['channel_id'] == channel_id), None)

    # Check if channel exists
    if channel is None:
        raise InputError('Channel_id does not exist')

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Check if authorisated user is an owner of the channel
    if not any(authorised_user['u_id'] == member['u_id'] and
               member['is_owner'] for member in channel['members']):
        raise AccessError(
            'Authorised user is not an owner of the channel')

    # Find the user from the selected channel, if user does not exists assigns None
    user = next(
        (member for member in channel['members'] if member['u_id'] == u_id), None)

    # If user does not exists creates a new member and addes it as an owner to the channel
    if user is None:
        user = next((user for user in users if user['u_id'] == u_id), None)
        new_owner = {
            'u_id': user['u_id'],
            'name_first': user['name_first'],
            'name_last': user['name_last'],
            'is_owner': True
        }
        channel['members'].append(new_owner)
    # Else check if the user is an owner, if they are throw and exception,
    # otherwise make them an owner
    else:
        if user['is_owner']:
            raise InputError(
                'User is already an owner of the channel')
        else:
            user['is_owner'] = True

    return {}


def channel_removeowner(token, channel_id, u_id):
    '''
    Remove user with user id u_id an owner of this channel
    '''

    channels = data['channels']
    users = data['users']

    # Finds the Channel, if it doesn't exists assigns None
    channel = next(
        (channel for channel in channels if channel['channel_id'] == channel_id), None)

    # If channel does not exist throw exception
    if channel is None:
        raise InputError('Channel_id does not exist')

    # Finds the user, if it doesn't exists assigns None
    user = next(
        (user for user in users if user['u_id'] == u_id), None)

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Check if authorisated user is an owner of the channel
    if not any(authorised_user['u_id'] == member['u_id']
               and member['is_owner'] for member in channel['members']):
        raise AccessError(
            'Authorised user is not an owner of the channel')

    # Find the user from the selected channel, if user does not exists assigns None
    owner = next((member for member in channel['members']
                  if user['u_id'] == member['u_id'] and member['is_owner']), None)

    # If user is not an owner of the channel throw exception
    if owner is None:
        raise InputError(
            'User with u_id is not an owner of the channel')
    # Else remove the owner as an owner of channel
    owner['is_owner'] = False

    return {}
