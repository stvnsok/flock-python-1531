def channel_invite(token, channel_id, u_id):
    return {
    } #Invites a user (with user id u_id) to join a channel with ID channel_id.
    # Once invited the user is added to the channel immediately

def channel_details(token, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }
    #Given a Channel with ID channel_id that the authorised user is part of, 
    # provide basic details about the channel




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
    return { # Given a channel ID, the user removed as a member of this channel
    }

def channel_join(token, channel_id):
    return { # Given a channel_id of a channel that the authorised user can join,
    #adds them to that channel
    }

def channel_addowner(token, channel_id, u_id):
    return { #Make user with user id u_id an owner of this channel
    }

def channel_removeowner(token, channel_id, u_id):
    return { # Remove user with user id u_id an owner of this channel
    }

def channel_list(token):
    return { # a list of all channels (and their associated details) that is 
    #authorised by the user
    }

def channel_lisall(token):
    return { # a list of all channels (and their associated details) no matter what
    }

def channel_create(token, name, is_public):
    
    return { # Creates a new channel with that name that is either a public or private channel
    }