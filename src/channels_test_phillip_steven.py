
#26/9/2020
#Phillip Law and Steven Sok
#Purpose: Test functions in channels.py

import pytest
import channel
import channels
from error import InputError

#all channels that user is part of
def test_channels_list():
    clear()
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
    

#all channels
def test_channels_listall():
    clear()
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
    

def test_channels_create():
    clear()
    result = channels.channels_create(1, channel1, True)
    assert result == {
        'channel_id': 1000
    }
    
    result = channels.channels_create(2, channel2, False)
    assert result == {
        'channel_id':2000
    }
    
