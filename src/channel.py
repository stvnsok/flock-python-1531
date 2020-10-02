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
    # channel['all_members'].append(new_member)

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
    '''Given a Channel with ID channel_id that the authorised user is part of, 
    return up to 50 messages between index "start" and "start + 50". Message with 
    index 0 is the most recent message in the channel. This function returns a new 
    index "end" which is the value of "start + 50", or, if this function has returned 
    the least recent messages in the channel, returns -1 in "end" to indicate there are
    no more messages to load after this return.'''

    channels = data['channels']
    users = data['users']

    # Finds the Channel, if it doesn't exists assigns None
    channel = next(
        (channel for channel in channels if channel['id'] == channel_id), None)

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Check if channel exists
    if (channel == None):
        raise InputError('Channel_id does not exist')

    # Check if authorised user is a member of the channel
    if not any(authorised_user['u_id'] == member['u_id'] for member in channel['all_members']):
        raise AccessError(
            'Authorised user is not a member of the channel')

    # sets the index for the last message
    end = start + 50
    messages = channel['messages']

    # if this index is greater than the amount of messages then
    # the amount of remaining messages after the start index
    # is less than 50
    if (len(channel['messages']) < end):
        end = -1
        messages = messages[start:]
    # send back messages between the start and end range
    else:
        messages = messages[start: end]

    # return result
    return {
        'messages': messages,
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
        (channel for channel in channels if channel['id'] == channel_id), None)

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Check if channel exists
    if (channel == None):
        raise InputError('Channel_id does not exist')

    # Check if authorised user is a member of the channel
    if not any(authorised_user['u_id'] == member['u_id'] for member in channel['all_members']):
        raise AccessError(
            'Authorised user is not a member of this channel')


    # member_number = 0
    # # Removal users from member -> make it more 'pythonic'?
    # for member in channel['all_members']:
    #     if authorised_user['u_id'] == member['u_id']:
    #         break
    #     member_number += 1

    # channel['all_members'].pop(member_number)
    

    # # Remove the user from owners
    # for member in channel['owner_members']:
    #     if authorised_user['u_id'] == member['u_id']:
    #         break
    #     member_number += 1

    # channel['owner_members'].pop(member_number)
    
    # Find the authorised user and remove them from the channel
    member = next(for member in channel['members'] if authorised_user['u_id'] == member['u_id'], None)

    channel['members'].pop(member)
    
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
        (channel for channel in channels if channel['id'] == channel_id), None)

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # Check if channel exists
    if (channel == None):
        raise InputError('Channel_id does not exist')

    # if (channel['id'] >= 9000):
    #     raise AccessError(
    #         'Authorised member is not owner of selected private channel')
    
    # channel['all_members'].append(authorised_user)

    # Determine whether channel is public or private
    # If channel is public, add them to the channel
    # Otherwise throw an exception
    if channel['is_public']:
           member = {
            'u_id': authorised_user['u_id'],
            'name_first': authorised_user['name_first'],
            'name_last': authorised_user['name_last'],
            'owner_member': False
            }
        channel['members'].append(member)
    else:
        raise AccessError(
            'Channel_id refers to a channel that is private')

    return {}

def channel_addowner(token, channel_id, u_id):
    #NOTES -> is the user exists but is not an 'owner' we make them an owner?

    '''
    Make user with user id u_id an owner of this channel
    '''

    channels = data['channels']
    users = data['users']

    # Finds the Channel, if it doesn't exists assigns None
    channel = next(
        (channel for channel in channels if channel['id'] == channel_id), None)

    # Finds the user, if it doesn't exists assigns None
    user = next(
        (user for user in users if user['u_id'] == u_id), None)

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # if any(user['u_id'] == member['u_id'] for member in channel['owner_members']):
    #     raise InputError(
    #         'User is already an owner of the channel')

    # if any(user['u_id'] == member['u_id'] for member in channel['members']):
    #     raise InputError(
    #         'User is already an owner of the channel')
    
    # Check if user to be add is not already an owner of the channel
    if any(user['u_id'] == member['u_id'] and member['is_owner'] for member in channel['members']):
        raise InputError(
            'User is already an owner of the channel')

    if (channel == None):
        raise InputError('Channel_id does not exist')

    # if not any(authorised_user['u_id'] == member['u_id'] for member in channel['owner_members']):
    #     raise AccessError(
    #         'Authorised user is not an owner of the channel')

    # Check if authorisated user is an owner of the channel
    if not any(authorised_user['u_id'] == member['u_id'] and member['is_owner'] for member in channel['members']):
        raise AccessError(
            'Authorised user is not an owner of the channel')

    member = {
            'u_id': user['u_id'],
            'name_first': user['name_first'],
            'name_last': user['name_last'],
            'is_owner': True
    }
    channel['members'].append(member)

    return {}

def channel_removeowner(token, channel_id, u_id):
    '''
    Remove user with user id u_id an owner of this channel
    '''

    channels = data['channels']
    users = data['users']
    
    # Finds the Channel, if it doesn't exists assigns None
    channel = next(
        (channel for channel in channels if channel['id'] == channel_id), None)

    # Finds the user, if it doesn't exists assigns None
    user = next(
        (user for user in users if user['u_id'] == u_id), None)

    # Get the user that is sending the request
    authorised_user = next(
        (user for user in users if user['token'] == token), None)

    # If channel does not exist throw exception
    if (channel == None):
        raise InputError('Channel_id does not exist')

    # If user is not an owner throw an exception
    if not any(user['u_id'] == member['u_id'] and member['is_owner'] for member in channel['members']):
        raise InputError(
            'User is not an owner of the channel')

    # Check if authorisated user is an owner of the channel
    if not any(authorised_user['u_id'] == member['u_id'] and member['is_owner'] for member in channel['members']):
        raise AccessError(
            'Authorised user is not an owner of the channel')

    # Find the member object for a given user from the members list in the channel object 
    member = next(member for member in channel['members'] if user['u_id'] == member['u_id'] and member['is_owner'], None)
    
    # If user is not an owner of the channel throw exception
    if member == None:
        raise AccessError(
            'User with u_id is not an owner of the channel')

    # member_number = 0
    # for member in channel['owner_members']:
    #     if user['u_id'] == member['u_id']:
    #         break
    #     member_number += 1
    
    # Remove member 
    channel['members'].pop(member)
    
    # # Or this
    # member['is_owner'] = False

    return {}
    