# Written on 24/09/2020
# Purpose to test functions in channel.py
import pytest
import channel
import channels
import auth
from error import InputError, AccessError
from other import clear

def test_channel():
    bruce = auth.auth_register('bruce@gmail.com', 'batm4n23', 'Bruce', 'Wayne')
    wayne = auth.auth_register('wayne@gmail.com', 'zorro#', 'Wayne', 'Thomas')
    alfred = auth.auth_register('alfred@gmail.com', 'wayneman0r', 'Alfred', 'Pennyworth')
    jack = auth.auth_register('jack@gmail.com', 'jkrsfunland', 'Jack', 'Napier')
    
    batcave_channel = channels.channels_create(bruce['token'], 'batcave_channel', True)
    manor_channel = channels.channels_create(wayne['token'], 'batcave_channel', False)

    ch_details = channel.channel_details(bruce['token'], batcave_channel['channel_id'])
    assert len(ch_details['owner_members']) == len(ch_details['all_members']) == 1

    # Test if members are added correctly when joining
    channel.channel_join(alfred['token'], batcave_channel['channel_id'])
    assert len(ch_details['all_members']) == 2

    with pytest.raises(InputError) as e:
        channel.channel_join(alfred['token'], 909)
    assert str(e.value) == 'Channel_id does not exist'

    with pytest.raises(AccessError) as e:
        channel.channel_join(alfred['token'], manor_channel['channel_id'])
    assert str(e.value) == 'Channel_id refers to a channel that is private'

    with pytest.raises(InputError) as e:
        channel.channel_addowner(wayne['token'], 909, alfred['u_id'])
    assert str(e.value) == 'Channel_id does not exist'
    
    with pytest.raises(AccessError) as e:
        channel.channel_addowner(wayne['token'], batcave_channel['channel_id'], alfred['u_id'])
    assert str(e.value) == 'Authorised user is not an owner of the channel'

    # Test if owners are added correctly
    channel.channel_addowner(bruce['token'], batcave_channel['channel_id'], alfred['u_id'])
    ch_details = channel.channel_details(bruce['token'], batcave_channel['channel_id'])
    assert len(ch_details['owner_members']) == 2

    with pytest.raises(InputError) as e:
        channel.channel_addowner(bruce['token'], batcave_channel['channel_id'], alfred['u_id'])
    assert str(e.value) == 'User is already an owner of the channel'

    with pytest.raises(InputError) as e:
        channel.channel_addowner(bruce['token'], 909, alfred['u_id'])
    assert str(e.value) == 'Channel_id does not exist'

    with pytest.raises(AccessError) as e:
        channel.channel_addowner(wayne['token'], batcave_channel['channel_id'], alfred['u_id'])
    assert str(e.value) == 'Authorised user is not an owner of the channel'

    channel.channel_join(jack['token'], batcave_channel['channel_id'])
    ch_details = channel.channel_details(bruce['token'], batcave_channel['channel_id'])
    assert len(ch_details['all_members']) == 3
    assert len(ch_details['owner_members']) == 2

    # Test channel_leave is implemented correctly 
    with pytest.raises(InputError) as e:
        channel.channel_leave(alfred['token'], 909)
    assert str(e.value) == 'Channel_id does not exist'

    with pytest.raises(AccessError) as e:
        channel.channel_leave(alfred['token'], manor_channel['channel_id'])
    assert str(e.value) == 'Authorised user is not a member of the channel'

    channel.channel_leave(alfred['token'], batcave_channel['channel_id'])
    ch_details = channel.channel_details(bruce['token'], batcave_channel['channel_id'])
    assert len(ch_details['all_members']) == 2
    assert len(ch_details['owner_members']) == 1

    # Test remove_owner
    channel.channel_addowner(bruce['token'], batcave_channel['channel_id'], jack['u_id'])
    ch_details = channel.channel_details(bruce['token'], batcave_channel['channel_id'])
    assert len(ch_details['owner_members']) == 2

    with pytest.raises(InputError) as e:
        channel.channel_removeowner(bruce['token'], batcave_channel['channel_id'], alfred['u_id'])
    assert str(e.value) == 'User with u_id is not an owner of the channel'

    with pytest.raises(AccessError) as e:
        channel.channel_removeowner(alfred['token'], batcave_channel['channel_id'], bruce['u_id'])
    assert str(e.value) == 'Authorised user is not an owner of the channel'

    with pytest.raises(InputError) as e:
        channel.channel_removeowner(alfred['token'], 909, bruce['u_id'])
    assert str(e.value) == 'Channel_id does not exist'

    channel.channel_removeowner(bruce['token'], batcave_channel['channel_id'], jack['u_id'])
    ch_details = channel.channel_details(bruce['token'], batcave_channel['channel_id'])
    assert len(ch_details['owner_members']) == 1

    clear()

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

    with pytest.raises(AccessError) as e:
        channel.channel_messages(bob['token'], cool_channel['channel_id'], 999)
    assert str(e.value) == 'Authorised user is not a member of the channel'
    
    # Check that there are no messages
    messages = channel.channel_messages(john['token'], cool_channel['channel_id'], 0)

    assert len(messages['messages']) == 0

    clear()

def test_channel_messages_start_greater():
    '''
    This test uses the feature channel/messages with an invalid start. The
    expected outcome is an error of 400 saying 'Start is greater than total
    number of messages'.
    '''
    user_1 = auth.auth_register("123@hotmail.com", "password", "Bobby", "McBob")
    new_channel = channels.channels_create(user_1['token'], 'channel_1', True)
    with pytest.raises(AccessError) as e:
        channel.channel_messages(user_1['token'], new_channel['channel_id'], 100)
    assert str(e.value) == 'Start is greater than total number of messages'
    
    clear()
def test_channel_messages_invalid_token():
    '''
    This test uses the feature channel/messages with an invalid token. The
    expected outcome is an error of 400 saying 'Token is incorrect'
    '''
    user_1 = auth.auth_register("123@hotmail.com", "password", "Bobby", "McBob")
    new_channel = channels.channels_create(user_1['token'], 'channel_1', True)
    with pytest.raises(AccessError) as e:
        channel.channel_messages("incorrect_token", new_channel['channel_id'], 0)
    assert str(e.value) == 'Token is incorrect'
    
    clear()
    
def test_channel_messages_working():
    '''
    This test uses the feature channel/messages to confirm
    all messages sent are stored correctly. 
    The expected outcome is dictories of messages, start, end.
    '''
    user_1 = auth.auth_register(
        "markowong2@hotmail.com",
        "markowong2",
        "marko2",
        "wong2"  
    )

    new_channel = channels.channels_create(user_1['token'], 'channel_1', True)

    for _ in range(20):
        message.message_send(user_1['token'], new_channel['channel_id'], "Hello" )
    
    response = channel.channel_messages(user_1['token'], new_channel['channel_id'], 0)
    
    assert response['end'] == -1
    
    for message in response['messages']:
        assert message['message'] == "Hello"
    
    for _ in range(100):
        message.message_send(user_1['token'], new_channel['channel_id'], "Goodbye")
    
    response = channel.channel_messages(user_1['token'], new_channel['channel_id'], 20)
    
    assert response['end'] == 70
    
    for message in response['messages']:
        assert message['message'] == "Goodbye"

    clear()

    
    
