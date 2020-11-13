'''
This acts as a 'database'. It will be initialised whenever a test is run (does not persist).

Dictionary layout

This is just to help build iteration 1 features and keep some consistency

User 0bject :  {
                    'u_id' : integer,
                    'email' : string,
                    'password' : string,
                    'name_first' : string,
                    'name_last' : string,
                    'handle_str' : string,
                    'token' : string,
                    'permission_id' : integer,
                    'profile_img_url' : string,
               }

Channel Object : {
                    'channel_id' : integer,
                    'name' : string,
                    'is_public' : boolean,
                    'members' : [
                                    {
                                        'u_id': integer,
                                        'name_first': string,
                                        'name_last': string,
                                        'is_owner': bool
                                    }

                                ],
                    'messages' : [
                                    {
                                        'message_id' : integer,
                                        'u_id' : integer,
                                        'message' : string,
                                        'time_created' : integer (unix timestamp),
                                        'reacts': [
                                            {
                                                'react_id': integer,
                                                'u_ids': [u_id, u_id...],                  
                                            }                                 

                                        ] 
                                        'is_pinned': bool
                                    }

                                ],
                 }

'''
data = {
    'users': [],
    'channels': [],
}

'''
Helper Functions that interface with the data dictionary
'''

def get_authorised_user(token):
    '''
    Get an authorised user based on token
    '''
    return next((user for user in data['users'] if user['token'] == token), None)

def get_user(u_id):
    '''
    Given a u_id returns a user
    '''
    u_id = int(u_id)
    return next((user for user in data['users'] if user['u_id'] == u_id), None)

def get_message(message_id, channel):
    '''
    Helper function that allows a message to be retrieved from a channel.
    Assumes message does exist and previous exceptions have been handled.
    '''
    message_id = int(message_id)
    for message in channel['messages']:
        if message['message_id'] == message_id:
            return message
    
    
def update_message(message_id, new_message, channel):
    '''
    Helper function to update a message quickly.
    Assumes message does exist and previous exceptions have been handled.
    '''
    message_id = int(message_id)
    for message in channel['messages']:
        if message['message_id'] == message_id:
            message = new_message
            return 

def get_channel(channel_id):
    '''
    Get the channel associated with the given channel_id
    '''
    channel_id = int(channel_id)
    return next((channel for channel in data['channels'] if channel['channel_id'] == channel_id), None)


def get_channel_with_message(message_id):
    '''
    Get the channel where the given message is.
    '''    
    message_id = int(message_id)
    return next((channel for channel in data['channels'] for message in channel['messages'] if message['message_id'] == message_id), None)


def channel_member(user, channel):
    '''
    See if a user is part of a channel
    '''
    
    return any(user['u_id'] == member['u_id'] for member in channel['members'])



def get_all_messages():
    '''
    Returns a list containing all the messages across all channels
    '''

    messages = []

    for channel in data['channels']:
        messages += channel['messages']
    
    return messages