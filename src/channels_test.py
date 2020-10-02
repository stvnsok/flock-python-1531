
#26/9/2020
#Phillip Law and Steven Sok
#Purpose: Test functions in channels.py

import pytest
import channel
import channels
from error import InputError

#all channels that user is part of
def test_channels_list():

    ''''
    result = channels.channels_list(1)
    assert result == {
        'channels': [
        	{
        		'channel_id': 1000,
        		'name': 'channel1',
        	},
            {
                'channel_id': 2000,
                'name': 'channel2',
            } 
        ]
    }
    
    result = channels.channels_list(2)
    assert result == {
            'channels': [
        	{
        		'channel_id': 1000,
        		'name': 'channel1',
        	},
            {
                'channel_id': 3000,
                'name': 'channel3',
            } 
        ]
    }    
    '''
    
    result = channels.channels_list(1)
    assert result == {}
    clear()
    
# user is not part of any channels?    
def test_no_channels():
#all channels
def test_channels_listall():

    '''
    result = channels.channels_listall(1)
    assert result == {
        'channels': [
        	{
        		'channel_id': 1000,
        		'name': 'channel1',
        	},
            {
                'channel_id': 2000,
                'name': 'channel2',
            },
            {
                'channel_id': 3000,
                'name': 'channel3',
            } 
        ]
    }
    '''
    result = channels.channels_listall(1)
    assert result == {}
    clear()
    
    
    clear()
    
def test_channels_create():

    with pytest.raises(InputError) as e:
        channel_id = channel_create(1, channel1, True)
    assert channel_id >= 1000 and channel_id <= 1999
    with pytest.raises(InputError) as e:
        channel_id = channels_creat(2, channel2, False)
    assert channel_id >= 9000
    
    clear()
