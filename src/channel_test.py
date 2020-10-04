# Written on 24/09/2020
# Purpose to test functions in channel.py
import pytest
import channel
import channels
import auth
from error import InputError, AccessError
from other import clear

# Test that public channel operates as expected
def test_channel_public():
    # Register users and have john set up a public channel
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    bob = auth.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime')
    cool_channel = channels.channels_create(john['token'], 'cool_channel', True)

    ch_details = channel.channel_details(john['token'], cool_channel['channel_id'])
    assert ch_details['name'] == 'cool_channel'
    assert len(ch_details['owner_members']) == len(ch_details['all_members']) == 1

    # Check that new members are being added correctly
    channel.channel_invite(john['token'], cool_channel['channel_id'], bob['u_id'])
    ch_details = channel.channel_details(john['token'], cool_channel['channel_id'])

    assert ch_details['name'] == 'cool_channel'
    assert len(ch_details['owner_members']) == 1
    assert len(ch_details['all_members']) == 2
    
    # Check that members can leave
    channel.channel_leave(bob['token'], cool_channel['channel_id'])
    ch_details = channel.channel_details(john['token'], cool_channel['channel_id'])
    assert len(ch_details['owner_members']) == 1 
    assert len(ch_details['all_members']) == 1
    
    # Check that members can join a public channel on their own
    channel.channel_join(bob['token'], cool_channel['channel_id'])
    ch_details = channel.channel_details(john['token'], cool_channel['channel_id'])
    assert len(ch_details['owner_members']) == 1 
    assert len(ch_details['all_members']) == 2

    clear()

# Test that private channel operates as expected
def test_channel_private():

    # Register three users and have John set up a private channel
    chicken = auth.auth_register("hehe@hotmail.com", "qwerty", "Chicken", "Nugget")
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    bob = auth.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime')
    private_cool_channel = channels.channels_create(john['token'], 'private_cool_channel', False)

    # Joining a private channel should throw an error
    with pytest.raises(AccessError) as e:
        channel.channel_join(chicken['token'], private_cool_channel['channel_id'])
    assert 'Channel_id refers to a channel that is private' == str(e.value)

    # John adds an Chicken as an owner of the private channel
    with pytest.raises(AccessError) as e:
        channel.channel_addowner(bob['token'], private_cool_channel['channel_id'], chicken['u_id'])
    assert 'Authorised user is not an owner of the channel' == str(e.value)

    # Add chicken correctly
    channel.channel_addowner(john['token'], private_cool_channel['channel_id'], chicken['u_id'])

    # Inputting the incorrect channel id
    with pytest.raises(InputError) as e:
        channel.channel_addowner(chicken['token'], 'incorrect_channel', bob['u_id'])
    assert 'Channel_id does not exist' == str(e.value)

    # Trying to invite a user that is already an owner 
    with pytest.raises(InputError) as e:
        channel.channel_addowner(chicken['token'], private_cool_channel['channel_id'], john['u_id'])
    assert 'User is already an owner of the channel' == str(e.value)
    
    # Allows user to invite people to private channel
    channel.channel_invite(chicken['token'], private_cool_channel['channel_id'], bob['u_id'])
    
    # Check details of channel, John, Chicken and Bob are all members,
    # John and Chicken are the only owners
    ch_details = channel.channel_details(chicken['token'], private_cool_channel['channel_id'])
    assert len(ch_details['owner_members']) == 2
    assert len(ch_details['all_members']) == 3
    assert ch_details['name'] == 'private_cool_channel'
    
    # Check that remove owner throw's correct exception
    with pytest.raises(InputError) as e:
        channel.channel_removeowner(john['token'], private_cool_channel['channel_id'], bob['u_id'])
    assert str(e.value) == 'User with u_id is not an owner of the channel'

    clear()


# Check channel_invite expections are working
def test_channel_invite_exceptions():
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    bob = auth.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime')
    cool_channel = channels.channels_create(john['token'], 'cool_channel', True)

    with pytest.raises(InputError) as e:
        channel.channel_invite(john['token'], 9999, bob['u_id'])
    assert str(e.value) == 'Channel_id does not exist'

    with pytest.raises(InputError) as e:
        channel.channel_invite(john['token'], cool_channel['channel_id'], 9999)
    assert str(e.value) == 'U_id does not exist'

    with pytest.raises(AccessError) as e:
        channel.channel_invite(bob['token'], cool_channel['channel_id'], john['u_id'])
    assert str(e.value) == 'Authorised user is not a member of the channel'
    
    clear()

# Check channel_detail expections are working
def test_channel_detail_exceptions():
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    bob = auth.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime')
    cool_channel = channels.channels_create(john['token'], 'cool_channel', True)

    with pytest.raises(InputError) as e:
        channel.channel_details(john['token'], 9999)
    assert str(e.value) == 'Channel_id does not exist'

    with pytest.raises(AccessError) as e:
        channel.channel_details(bob['token'], cool_channel['channel_id'])
    assert str(e.value) == 'Authorised user is not a member of the channel'
    
    clear()

# Check channel_leave exceptions are working
def test_channel_leave_exceptions():
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    bob = auth.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime')
    cool_channel = channels.channels_create(john['token'], 'cool_channel', True)

    with pytest.raises(InputError) as e:
        channel.channel_leave(john['token'], 9999)
    assert str(e.value) == 'Channel_id does not exist'

    with pytest.raises(AccessError) as e:
        channel.channel_leave(bob['token'], cool_channel['channel_id'])
    assert str(e.value) == 'Authorised user is not a member of the channel'
    
    clear()

# Check channel_leave exceptions are working
def test_channel_join_exceptions():
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    bob = auth.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime')
    cool_channel = channels.channels_create(john['token'], 'cool_channel', False)

    with pytest.raises(InputError) as e:
        channel.channel_join(john['token'], 9999)
    assert str(e.value) == 'Channel_id does not exist'

    with pytest.raises(AccessError) as e:
        channel.channel_join(bob['token'], cool_channel['channel_id'])
    assert str(e.value) == 'Channel_id refers to a channel that is private'
    
    clear()

# Check channel_addowner exceptions are working
def test_channel_addowner_exceptions():
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    bob = auth.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime')
    lucy = auth.auth_register('lucy@gmail.com', 'asd123!@#', 'Lucy', 'Lime')
    cool_channel = channels.channels_create(john['token'], 'cool_channel', True)

    with pytest.raises(InputError) as e:
        channel.channel_addowner(john['token'], 9999 , bob['u_id'])
    assert str(e.value) == 'Channel_id does not exist'
   
    channel.channel_addowner(john['token'], cool_channel['channel_id'], bob['u_id'])
    
    with pytest.raises(InputError) as e:
        channel.channel_addowner(john['token'], cool_channel['channel_id'], bob['u_id'])
    assert str(e.value) == 'User is already an owner of the channel'
    
    with pytest.raises(AccessError) as e:
        channel.channel_addowner(lucy['token'], cool_channel['channel_id'], bob['u_id'])
    assert str(e.value) == 'Authorised user is not an owner of the channel'

    clear()
# Check channel_removeowner exceptions are working
def test_channel_removeowner_exceptions():
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    bob = auth.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime')
    lucy = auth.auth_register('lucy@gmail.com', 'asd123!@#', 'Lucy', 'Lime')
    cool_channel = channels.channels_create(john['token'], 'cool_channel', True)

    with pytest.raises(InputError) as e:
        channel.channel_removeowner(john['token'], 9999 , bob['u_id'])
    assert str(e.value) == 'Channel_id does not exist'
       
    with pytest.raises(InputError) as e:
        channel.channel_removeowner(john['token'], cool_channel['channel_id'], bob['u_id'])
    assert str(e.value) == 'User with u_id is not an owner of the channel'
    
    with pytest.raises(AccessError) as e:
        channel.channel_removeowner(lucy['token'], cool_channel['channel_id'], john['u_id'])
    assert str(e.value) == 'Authorised user is not an owner of the channel'

    clear()


# Check channel_messages is working
def test_channel_messages():
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    bob = auth.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime')
    cool_channel = channels.channels_create(john['token'], 'cool_channel', False)
    
    # Check exceptions
    with pytest.raises(InputError) as e:
        channel.channel_messages(john['token'], 9999, 0)
    assert str(e.value) == 'Channel_id does not exist'

    with pytest.raises(InputError) as e:
        channel.channel_messages(john['token'], cool_channel['channel_id'], 999)
    assert str(e.value) == 'Start is greater than total number of messages'

    with pytest.raises(AccessError) as e:
        channel.channel_messages(bob['token'], cool_channel['channel_id'], 999)
    assert str(e.value) == 'Authorised user is not a member of the channel'
    
    # Check that there are no messages
    messages = channel.channel_messages(john['token'], cool_channel['channel_id'], 0)

    assert len(messages['messages']) == 0

    clear()