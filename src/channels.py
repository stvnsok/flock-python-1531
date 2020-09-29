'''
channels_list
Provide a list of all channels (and their associated details) that the authorised user is part of
Parameters: (token)
Return type: {channels}
Exceptions: N/A
'''

def channels_list(token):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

'''
channels_listall
Provide a list of all channels (and their associated details)
Parameters: (token)
Return type: {channels}
Exceptions: N/A
'''

def channels_listall(token):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

'''
channels_create
Creates a new channel with that name that is either a public or private channel
Parameters: (token, name, is_public)
Return type: {channel_id}
Exceptions: InputError when the name of the channel exceeds 20 characters
'''

def channels_create(token, name, is_public):
    return {
        'channel_id': 1,
    }
