
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
        		'name': 'Channel1',
        	},
            {
                'channel_id': 2000,
                'name': 'Channel2',
            } 
        ]
    }
    
    result = channels.channels_list(2)
    assert result == {
            'channels': [
        	{
        		'channel_id': 1000,
        		'name': 'Channel1',
        	},
            {
                'channel_id': 3000,
                'name': 'Channel3',
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
        		'name': 'Channel1',
        	},
            {
                'channel_id': 2000,
                'name': 'Channel2',
            },
            {
                'channel_id': 3000,
                'name': 'Channel3',
            } 
        ]
    }
    
'''
def test_channels_create():


#test no channels joined
def test_channels_none():

'''
