# Written on 24/09/2020 
# By Marko Wong (z5309371)
# Purpose to test functions in channel.py
import pytest
import channel
import channels
from error import InputError
'''def test_channel_create_public():
    channel_id = channel_create("token", "name", True)
    assert channel_id >= 1000 and channel_id <= 1999

def test_channel_create_private():
    channel_id = channel_create("token", "It's over 9000 Nani!", False)
    assert channel_id >= 9000 and channel_id <= 9999

def test_channel_create_multiple():
    for channels_id in range(1000,1006):
        assert channel_create("token", "name" + str(channels_id), True) == channels_id
    
# May need to test for valid tokens but tokens not implemented yet '''

def test_invite_to_invalid_channel():
    channels.channels_create(login['token'], "channel_1", True)
    

