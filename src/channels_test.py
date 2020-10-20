#26/9/2020
#Purpose: Test functions in channels.py

import pytest
import auth
import channel
import channels
from data import data 
from other import clear
from error import InputError, AccessError

#---------------------Testing channels_list function with:---------------------#
# incorrect token
def test_channels_list_invalid_token():
    user = auth.auth_register('john@hotmail.com', 'qwe123!@#', 'John', 'Smith')
    token = user['token']
    with pytest.raises(AccessError) as e:
        channels.channels_list("invalid_token")
    assert 'Token is incorrect/user does not exist' == str(e.value)
    clear()

# no existing channels
def test_channels_list_no_channels():
    user = auth.auth_register("123@hotmail.com", "password", "Bobby", "McBob")
    token = user['token']
    assert channels.channels_list(token) == {'channels': []}
    clear()

# 1 exiting channel
def test_channels_list_one():
    user = auth.auth_register("123@hotmail.com", "password", "Bobby", "McBob")
    token = user['token']
    channels.channels_create(token,"channel_1", True)
    assert channels.channels_list(token) == {'channels': [
        {'channel_id': 1, 
        'is_public': True,
        'members': [{
            'is_owner': True,
            'name_first': 'Bobby',
            'name_last': 'McBob',
            'u_id': 1}],
        'messages': [],
        'name': 'channel_1'}],
        }
    clear()


# 3 exisiting channels
def test_channels_list_three():
    user = auth.auth_register("123@hotmail.com", "password", "Bobby", "McBob")
    token = user['token']
    channels.channels_create(token,"channel_1", True)
    channels.channels_create(token,"channel_2", False)
    channels.channels_create(token,"channel_3", True)
    assert channels.channels_list(token) == {'channels': [
        {'channel_id': 1, 
        'is_public': True,
        'members': [{
            'is_owner': True,
            'name_first': 'Bobby',
            'name_last': 'McBob',
            'u_id': 1}],
        'messages': [],
        'name': 'channel_1'},
        {'channel_id': 2,
        'is_public': False,
        'members': [{'is_owner': True,
            'name_first': 'Bobby',
            'name_last': 'McBob',
            'u_id': 1}],
        'messages': [],
        'name': 'channel_2'},
        {'channel_id': 3,
        'is_public': True,
        'members': [{'is_owner': True,
            'name_first': 'Bobby',
            'name_last': 'McBob',
            'u_id': 1}],
        'messages': [],
        'name': 'channel_3'}],
    }
    clear()

# one channel the user is not part of 
def test_channels_list_not_in():
    user1 = auth.auth_register("123@hotmail.com", "password", "Bobby", "McBob")
    token1 = user1['token']
    channels.channels_create(token1,"channel_1", True)
    user2 = auth.auth_register("bestanime@hotmail.com", "Goku is mid!", "mei", "wei")
    token2 = user2['token']
    channels.channels_create(token2,"channel_2", False)
    assert channels.channels_list(token2) == {'channels': [
        {'channel_id': 2, 
        'is_public': False,
        'members': [{
            'is_owner': True,
            'name_first': 'mei',
            'name_last': 'wei',
            'u_id': 2}],
        'messages': [],
        'name': 'channel_2'}],
        }
    clear()
    
# user not part of any channels with existing channels
def test_channels_list_user_in_no_channels():
    user1 = auth.auth_register("123@hotmail.com", "password", "Bobby", "McBob")
    token1 = user1['token']
    channels.channels_create(token1,"channel_1", True)
    channels.channels_create(token1,"channel_2", False)
    channels.channels_create(token1,"channel_3", True)
    channels.channels_create(token1,"channel_4", False)
    user2 = auth.auth_register("bestanime@hotmail.com", "Goku is mid!", "mei", "wei")
    token2 = user2['token']
    assert channels.channels_list(token2) == {'channels': []}
    clear()

#---------------------Testing channels_listall function with:------------------#
# incorrect token
def test_channels_listall_invalid_token():
    user = auth.auth_register('john@hotmail.com', 'qwe123!@#', 'John', 'Smith')
    token = user['token']
    with pytest.raises(AccessError) as e:
        channels.channels_listall("invalid_token")
    assert 'Token is incorrect/user does not exist' == str(e.value)
    clear()

# no existing channels
def test_channels_listall_no_channels():
    user = auth.auth_register("123@hotmail.com", "password", "Bobby", "McBob")
    token = user['token']
    assert channels.channels_listall(token) == {'channels': []}
    clear()

# 1 exiting channel
def test_channels_listall_one():
    user = auth.auth_register("123@hotmail.com", "password", "Bobby", "McBob")
    token = user['token']
    channels.channels_create(token,"channel_1", True)
    assert channels.channels_listall(token) == {'channels': [
        {'channel_id': 1, 
        'is_public': True,
        'members': [{
            'is_owner': True,
            'name_first': 'Bobby',
            'name_last': 'McBob',
            'u_id': 1}],
        'messages': [],
        'name': 'channel_1'}],
        }
    clear()


# 3 exisiting channels
def test_channels_listall_three():
    user = auth.auth_register("123@hotmail.com", "password", "Bobby", "McBob")
    token = user['token']
    channels.channels_create(token,"channel_1", True)
    channels.channels_create(token,"channel_2", False)
    channels.channels_create(token,"channel_3", True)
    assert channels.channels_listall(token) == {'channels': [
        {'channel_id': 1, 
        'is_public': True,
        'members': [{
            'is_owner': True,
            'name_first': 'Bobby',
            'name_last': 'McBob',
            'u_id': 1}],
        'messages': [],
        'name': 'channel_1'},
        {'channel_id': 2,
        'is_public': False,
        'members': [{'is_owner': True,
            'name_first': 'Bobby',
            'name_last': 'McBob',
            'u_id': 1}],
        'messages': [],
        'name': 'channel_2'},
        {'channel_id': 3,
        'is_public': True,
        'members': [{'is_owner': True,
            'name_first': 'Bobby',
            'name_last': 'McBob',
            'u_id': 1}],
        'messages': [],
        'name': 'channel_3'}],
    }
    clear()

# one channel the user is not part of 
def test_channels_listall_not_in():
    user1 = auth.auth_register("123@hotmail.com", "password", "Bobby", "McBob")
    token1 = user1['token']
    channels.channels_create(token1,"channel_1", True)
    user2 = auth.auth_register("bestanime@hotmail.com", "Goku is mid!", "mei", "wei")
    token2 = user2['token']
    channels.channels_create(token2,"channel_2", False)
    assert channels.channels_listall(token2) == {'channels': [
        {'channel_id': 1, 
        'is_public': True,
        'members': [{
            'is_owner': True,
            'name_first': 'Bobby',
            'name_last': 'McBob',
            'u_id': 1}],
        'messages': [],
        'name': 'channel_1'},
        {'channel_id': 2, 
        'is_public': False,
        'members': [{
            'is_owner': True,
            'name_first': 'mei',
            'name_last': 'wei',
            'u_id': 2}],
        'messages': [],
        'name': 'channel_2'}],
        }
    clear()
    
# user not part of any channels with existing channels
def test_channels_listall_user_in_no_channels():
    user1 = auth.auth_register("123@hotmail.com", "password", "Bobby", "McBob")
    token1 = user1['token']
    channels.channels_create(token1,"channel_1", True)
    channels.channels_create(token1,"channel_2", False)
    channels.channels_create(token1,"channel_3", True)
    user2 = auth.auth_register("bestanime@hotmail.com", "Goku is mid!", "mei", "wei")
    token2 = user2['token']
    assert channels.channels_listall(token2) == {'channels': [
        {'channel_id': 1, 
        'is_public': True,
        'members': [{
            'is_owner': True,
            'name_first': 'Bobby',
            'name_last': 'McBob',
            'u_id': 1}],
        'messages': [],
        'name': 'channel_1'},
        {'channel_id': 2,
        'is_public': False,
        'members': [{'is_owner': True,
            'name_first': 'Bobby',
            'name_last': 'McBob',
            'u_id': 1}],
        'messages': [],
        'name': 'channel_2'},
        {'channel_id': 3,
        'is_public': True,
        'members': [{'is_owner': True,
            'name_first': 'Bobby',
            'name_last': 'McBob',
            'u_id': 1}],
        'messages': [],
        'name': 'channel_3'}],
    }
    clear()

#--------------------Testing channels_create function for:---------------------#
# incorrect token
def test_channels_create_invalid_token():
    user = auth.auth_register('john@hotmail.com', 'qwe123!@#', 'John', 'Smith')
    token = user['token']
    with pytest.raises(AccessError) as e:
        channels.channels_create("invalid_token", "name", True)
    assert 'Token is incorrect/user does not exist' == str(e.value)
    clear()

# invalid name
def test_channels_create_invalid_name():
    user = auth.auth_register('john@hotmail.com', 'qwe123!@#', 'John', 'Smith')
    token = user['token']
    with pytest.raises(InputError) as e:
        channels.channels_create(token, "Hatsune Miku is best Waifu, FIGHT ME!", True)
    assert 'Input Channel Name too long' == str(e.value)
    clear()

# 1000 channel creation
def test_channels_create_lots():
    user = auth.auth_register('john@hotmail.com', 'qwe123!@#', 'John', 'Smith')
    token = user['token']
    for no_of_channels in range(1000):
        channel = channels.channels_create(token, "No, I'm spiderman", True)
        id = channel['channel_id']
        assert id == (no_of_channels + 1)
    assert id == 1000
    clear()

# correct is_public status
def test_channels_create_is_public():
    user = auth.auth_register('john@hotmail.com', 'qwe123!@#', 'John', 'Smith')
    token = user['token']
    channels.channels_create(token, "No, I'm spiderman", True)
    list_channels = data['channels']
    assert list_channels[0]['is_public'] == True
    channels.channels_create(token, "cult of spidermans", False)
    assert list_channels[1]['is_public'] == False
    clear()

# creator got added to channnel as owner
def test_channels_create_owner():
    user = auth.auth_register('john@hotmail.com', 'qwe123!@#', 'John', 'Smith')
    token = user['token']
    channels.channels_create(token, "Anime Betrayals", True)
    list_channels = data['channels']
    assert list_channels[0]['members'][0]['is_owner'] == True
    
