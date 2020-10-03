# Written on 24/09/2020
# Purpose to test functions in channel.py
import pytest
import channel
import channels
import auth
from error import InputError, AccessError
from other import clear

def test_channel_1():
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    bob = auth.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime')
    cool_channel = channels.channels_create(john['token'], 'cool_channel', True)

    ch_details = channel.channel_details(john['token'], cool_channel['channel_id'])
    assert ch_details['name'] == 'cool_channel'
    assert len(ch_details['owner_members']) == len(ch_details['all_members']) == 1

    with pytest.raises(InputError) as e:
        channel.channel_invite(john['token'], 9999, bob['u_id'])
    assert str(e.value) == 'Channel_id does not exist'

    with pytest.raises(InputError) as e:
        channel.channel_invite(john['token'], cool_channel['channel_id'], 9999)
    assert str(e.value) == 'U_id does not exist'

    with pytest.raises(AccessError) as e:
        channel.channel_invite(bob['token'], cool_channel['channel_id'], john['u_id'])
    assert str(e.value) == 'Authorised user is not a member of the channel'

    channel.channel_invite(john['token'], cool_channel['channel_id'], bob['u_id'])
    ch_details = channel.channel_details(john['token'], cool_channel['channel_id'])

    assert ch_details['name'] == 'cool_channel'
    assert len(ch_details['owner_members']) == 1
    assert len(ch_details['all_members']) == 2
    
    channel.channel_leave(bob['token'], cool_channel['channel_id'])
    ch_details = channel.channel_details(john['token'], cool_channel['channel_id'])
    assert len(ch_details['owner_members']) == len(ch_details['all_members']) == 1

    channel.channel_addowner(john['token'], cool_channel['channel_id'], bob['u_id'])
    ch_details = channel.channel_details(john['token'], cool_channel['channel_id'])
    assert len(ch_details['owner_members']) == len(ch_details['all_members']) == 2

    channel.channel_removeowner(john['token'], cool_channel['channel_id'], bob['u_id'])
    ch_details = channel.channel_details(john['token'], cool_channel['channel_id'])
    assert len(ch_details['owner_members']) == 1
    assert len(ch_details['all_members']) == 2

    clear()

def test_channel_details():
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    cool_channel = channel.channel_create(john['token'], 'cool_channel', True)
    
    ch_details = channel.channel_details(john['token'], cool_channel['channel_id'])
    assert len(ch_details['owner_members']) == len(ch_details['all_members']) == 1

    clear()


# Test invalid token for channel_invite
    user = auth.auth_register("hehe@hotmail.com", "qwerty", "Chicken", "Nugget")
    token = user['token']
    with pytest.raises(AccessError) as e:
        channel.channel_invite("invalid_token")
    assert 'Token is incorrect/user does not exist' == str(e.value)
    
    
# Test invalid channel exception
def test_channel_invite_invalid_channel():
    with pytest.raises(InputError) as e:
         channel.channel_invite(fried['token'], food_channel['channel_id'], chicken['u_id'])
    assert 'Channel_id does not exist' == str(e.value)
    clear()

# Test invalid u_id exception
def test_channel_invite_invalid_user():
    with pytest.raises(InputError) as e:
        channel.channel_invite(john['token'], cool_channel['channel_id'], bob['u_id'])
    assert 'The u_id is invalid' == str(e.value)
    clear()
    
# Test unauthorised user exception
def test_channel_invite_unauthorised_user():
    with pytest.raises(AccessError) as e:
        channel.channel_invite(fried['token'], food_channel['channel_id'], chicken['u_id'])
    assert 'Authorised user is not a member of the channel' == str(e.value) 
    clear()

# Test invalid token for channel_details
def test_channel_details_invalid():
    user = auth.auth_register("hehe@hotmail.com", "qwerty", "Chicken", "Nugget")
    token = user['token']
    with pytest.raises(AccessError) as e:
        channel.channel_details("invalid_token")
    assert 'Token is incorrect/user does not exist' == str(e.value)
    
    clear()
    
# Test channel details
def test_channel_details():
    user = auth.auth_register("hehe@hotmail.com", "qwerty", "Chicken", "Nugget")
    token = user['token']
    assert channel.channel_details(token) == { 
        'name': 'channel_1',
        'owner_members': [{
            'u_id': 1,
            'name_first': 'Chicken',
            'name_last': 'Nugget'}],
        'all_members': [{
            'u_id': 1,
            'name_first': 'Chicken',
            'name_last': 'Nugget',
            'u_id': 2,
            'name_first': 'Zinger',
            'name_last': 'Box',
            'u_id': 3,
            'name_first': 'Wicked',
            'name_last': 'Wings'}]   
    }
    clear()
    
# Test no channel details
def test_channel_details_none():
    user = auth.auth_register("hehe@hotmail.com", "qwerty", "Chicken", "Nugget")
    token = user['token']
    assert channel.channel_details(token) == {
        'name': [],
        'owner_members': [],
        'all_members': []
    }
    clear()           
    
# Test invalid channel
def test_channel_details_invalid_channel():
    user = auth.auth_register("hehe@hotmail.com", "qwerty", "Chicken", "Nugget")
    token = user['token']
    with pytest.raises(InputError) as e:
        channel.channel_details(token, "999" )
    assert 'Channel is invalid/does not exist' == str(e.value)
    clear()

# Test an unauthorised member
def test_channel_details_unauthorised_user():
    with pytest.raises(AccessError) as e:
        channel.channel_details(fried['token'], food_channel['channel_id'], chicken['u_id'])
    assert 'Authorised user is not a member of the channel' == str(e.value)
    clear()
    
# Test invalid token for channel_join
def test_channel_removeowner_invalid_token():
    user = auth.auth_register("hehe@hotmail.com", "qwerty", "Chicken", "Nugget")
    with pytest.raises(AccessError) as e:
        channel.channel_join("invalid_token")
    assert 'Token is incorrect/user does not exist' == str(e.value)
    clear()
# Test invalid token for channel_leave
def test_channel_removeowner_invalid_token():
    user = auth.auth_register("hehe@hotmail.com", "qwerty", "Chicken", "Nugget")
    with pytest.raises(AccessError) as e:
        channel.channel_leave("invalid_token")
    assert 'Token is incorrect/user does not exist' == str(e.value)
    clear()
# Test invalid token for channel_addowner
def test_channel_removeowner_invalid_token():
    user = auth.auth_register("hehe@hotmail.com", "qwerty", "Chicken", "Nugget")
    with pytest.raises(AccessError) as e:
        channel.channel_addowner("invalid_token")
    assert 'Token is incorrect/user does not exist' == str(e.value)
    clear()
# Test invalid token for channel_removeowner
def test_channel_removeowner_invalid_token():
    user = auth.auth_register("hehe@hotmail.com", "qwerty", "Chicken", "Nugget")
    with pytest.raises(AccessError) as e:
        channel.channel_removeowner("invalid_token")
    assert 'Token is incorrect/user does not exist' == str(e.value)
    clear()

