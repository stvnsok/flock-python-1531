def channels_list(token):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_listall(token):
    return {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'My Channel',
        	}
        ],
    }

def channels_create(token, name, is_public):

    new_channel = {
        'channel_id': len(channels)
        ''
    }

    return {
        'channel_id': 1,
    }
