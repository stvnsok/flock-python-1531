
#26/9/2020
#Purpose: Test functions in channels.py

import pytest
import auth
import channel
import channels
from data import data 
from other import clear
from error import InputError

# testing channel_list function with:
# no existing channels
def test_channels_list_no_channels():
    result = auth.auth_register("123@hotmail.com", "password", "Bobby", "McBob")
    token = result['token']
    assert channels.channels_list(token) == {'channels': []}
    clear()

# 3 exiting channel
def test_channels_list_one():
    users = data['users']
    result = auth.auth_register("123@hotmail.com", "password", "Bobby", "McBob")
    token = result['token']
    channels.channels_create(token,"channel_1", True)
    channels.channels_create(token,"channel_2", True)
    channels.channels_create(token,"channel_3", True)
    assert channels.channels_list(token) == {'channels': []}

'''   
# user is not part of any channels?    
def test_no_channels():
#all channels
def test_channels_listall():

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
'''