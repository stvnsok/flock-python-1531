'''
Tests for message.py
Written on 15/10/2020
'''
import pytest
from datetime import datetime, timedelta
import auth
import channel
import channels
import message
from error import InputError, AccessError
import other
from data import create_token

invalid_token = create_token(999999)

def test_message_send_length():
    '''
    Throws an InputError if they message is longer than 1000 characters
    '''

    john = auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    john_channel = channels.channels_create(
        john['token'], 'john_channel', True)

    long_message = """Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
    nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
    reprehenderit in voluptate velit esse cillum dolore eu fugiat 
    nulla pariatur. Excepteur sint occaecat cupidatat non proident, 
    sunt in culpa qui officia deserunt mollit anim id est laborum.
    Sed ut perspiciatis unde omnis iste natus error sit voluptatem 
    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa 
    quae ab illo inventore veritatis et quasi architecto beatae vitae 
    dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit 
    aspernatur aut odit aut fugit, sed quia consequuntur magni dolores 
    eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, 
    qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, 
    sed quia non numquam eius modi tempora incidunt ut labore et dolore 
    magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis 
    nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut 
    aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit 
    qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum 
    qui dolorem eum fugiat quo voluptas nulla pariatur?"""

    with pytest.raises(InputError) as e:
        message.message_send(
            john['token'], john_channel['channel_id'], long_message)

    assert str(e.value) == '400 Bad Request: Message is more than 1000 characters'    

    other.clear()


def test_message_uninvited_user():
    '''
    Throws an access error if a user that has not joined the channel tries to post a message
    '''
    
    john = auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    bob = auth.auth_register(
        'bob@gmail.com', 'abc123!@#', 'Bob', 'Lime')

    bob_channel = channels.channels_create(
        bob['token'], 'bob_channel', True)

    impossible_message = "I dont think I belong here"
       
    with pytest.raises(AccessError) as e:
        message.message_send(
            john['token'], bob_channel['channel_id'], impossible_message)

    assert str(e.value) == '400 Bad Request: Authorised user has not joined this channel yet'   

    other.clear()


def test_message_send_and_remove():
    '''
    Tests whether a valid message is stored correctly and can be removed
    '''

    john = auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    john_channel = channels.channels_create(
        john['token'], 'john_channel', True)
    
    valid_message = "Hello"
    message_sent_john = message.message_send(
        john['token'], john_channel['channel_id'], valid_message)

    response = message.message_remove(john['token'], message_sent_john['message_id'])

    assert response == {}

    other.clear()


def test_message_remove_invalid_id():
    '''
    Throws an Input error if the message based on ID no longer exists
    '''
    
    john = auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')

    with pytest.raises(InputError) as e:
        message.message_remove(john['token'], 9999)

    assert str(e.value) == '400 Bad Request: Message does not exist'

    with pytest.raises(InputError) as e:
        message.message_edit(john['token'], 9999, "Goodbye")

    assert str(e.value) == '400 Bad Request: Message does not exist'

    other.clear()
    

def test_message_unauthorised_user():
    '''
    Throws an AccessError if the message id does not map to a message 
    sent by the authorised user
    '''

    bob = auth.auth_register(
        'bob@gmail.com', 'abc123!@#', 'Bob', 'Lime')
    sally = auth.auth_register(
        'sally@gmail.com', 'Helo123!', 'Sally', 'Lemon')

    bob_channel = channels.channels_create(
        bob['token'], 'bob_channel', True)
   
    message_sent = message.message_send(
        bob['token'], bob_channel['channel_id'], "Hello")

    with pytest.raises(AccessError) as e:
        message.message_remove(
            sally['token'], message_sent['message_id'])

    assert str(e.value) == '400 Bad Request: Message to remove was not sent by authorised user. Authorised user is not an owner of the channel'

    with pytest.raises(AccessError) as e:
        message.message_edit(
            sally['token'], message_sent['message_id'], "Goodbye")

    assert str(e.value) == '400 Bad Request: Message to remove was not sent by authorised user. Authorised user is not an owner of the channel'

    other.clear()



def test_message_user_permissions():
    '''
    Test that John as an owner of Flockr cannot delete/edit messages even though he has global
    permissions because he is not in the channel Bob set up
    '''

    john = auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    bob = auth.auth_register(
        'bob@gmail.com', 'abc123!@#', 'Bob', 'Lime')

    bob_channel = channels.channels_create(
        bob['token'], 'bob_channel', True)

    message_sent = message.message_send(
        bob['token'], bob_channel['channel_id'], "Hello")

    with pytest.raises(AccessError) as e:
        message.message_remove(
            john['token'], message_sent['message_id'])

    assert str(e.value) == '400 Bad Request: Message to remove was not sent by authorised user. Authorised user is not an owner of the channel'

    with pytest.raises(AccessError) as e:
        message.message_edit(
            john['token'], message_sent['message_id'], "Goodbye")

    assert str(e.value) == '400 Bad Request: Message to remove was not sent by authorised user. Authorised user is not an owner of the channel'

    other.clear()


def test_message_edit_edited():
    '''
    Test that a message sent can be edited successfully and correctly
    '''

    john = auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    john_channel = channels.channels_create(
        john['token'], 'john_channel', True)

    old_message = "This is the old message"
    message_sent_john = message.message_send(
        john['token'], john_channel['channel_id'], old_message)

    message_in_data = other.search(john['token'], "This is the") 

    assert message_in_data['messages'][0]['message'] == old_message

    new_message = "This is the new message"
    message.message_edit(
        john['token'], message_sent_john['message_id'], new_message)


    message_in_data = other.search(john['token'], "This is the new message") 

    assert message_in_data['messages'][0]['message'] == new_message

    other.clear()


def test_message_edit_delete():
    '''
    Test that a message sent can be deleted successfully if nothing is passed
    '''

    john = auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    john_channel = channels.channels_create(
        john['token'], 'john_channel', True)

    old_message = "This is the old message"
    message_sent_john = message.message_send(
        john['token'], john_channel['channel_id'], old_message)

    message_in_data = other.search(john['token'], "This is the") 

    assert message_in_data['messages'][0]['message'] == old_message

    new_message = ""
    assert message.message_edit(
        john['token'], message_sent_john['message_id'], new_message) == {}

    message_in_data = other.search(john['token'], new_message) 

    assert len(message_in_data['messages']) == 0

    other.clear()


def test_message_sendlater_invalid_time():
    '''
    Test that a message sent with past timestamp throws error
    '''

    john = auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    john_channel = channels.channels_create(
        john['token'], 'john_channel', True)

    future_message = "This is a message from the past"
    future_date = datetime.now() + timedelta(days=-4) 
    future_date = future_date.timestamp()

    with pytest.raises(InputError) as e:
        message.message_sendlater(john['token'], john_channel['channel_id'], future_message, future_date)

    assert str(e.value) == '400 Bad Request: Time sent is a time in the past'

    other.clear()



def test_message_sendlater_invalid_user():
    '''
    Test that a message sent from unauthorised user throws error
    '''

    john = auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    bob = auth.auth_register(
        'bob@gmail.com', 'qwe123!@#', 'Bob', 'Smith')
    john_channel = channels.channels_create(
        john['token'], 'john_channel', True)

    future_message = "This is a message from the past"
    future_date = datetime.now() + timedelta(days=4) 
    future_date = future_date.timestamp()

    with pytest.raises(AccessError) as e:
        message.message_sendlater(bob['token'], john_channel['channel_id'], future_message, future_date)
    
    assert str(e.value) == '400 Bad Request: Authorised user has not joined the channel'

    other.clear()
    

def test_message_sendlater():
    '''
    Test that a message sent with past timestamp throws error
    '''

    john = auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')

    john_channel = channels.channels_create(
        john['token'], 'john_channel', True)

    future_message = "This is a message for the future"
    future_date = datetime.now() + timedelta(days=4) 
    future_date = future_date.timestamp()

    response = message.message_sendlater(john['token'], john_channel['channel_id'], future_message, future_date)

    assert response['message_id'] == 0

    other.clear()


def test_react_invalid_message():
    '''
    Tests that error is thrown then message_id is not within channel
    BOTH FOR REACT AND UNREACT
    '''

    john = auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')

    channels.channels_create(
        john['token'], 'john_channel', True)

    with pytest.raises(InputError) as e:
        message.message_react(john['token'], 9999999, 1)

    assert str(e.value) == '400 Bad Request: Message_id is not a valid message within a channel that the authorised user has joined'

    with pytest.raises(InputError) as e:
        message.message_unreact(john['token'], 9999999, 1)

    assert str(e.value) == '400 Bad Request: Message_id is not a valid message within a channel that the authorised user has joined'

    other.clear()


    

def test_react_invalid_react_id():
    '''
    Tests that error is thrown when react_id is not correct
    BOTH FOR REACT AND UNREACT
    '''

    john = auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')

    with pytest.raises(InputError) as e:
        message.message_react(john['token'], 9999999, 100)

    assert str(e.value) == '400 Bad Request: React_id is not a valid React ID'
    
    with pytest.raises(InputError) as e:
        message.message_unreact(john['token'], 9999999, 100)

    assert str(e.value) == '400 Bad Request: React_id is not a valid React ID'

    other.clear()


    

def test_react():
    '''
    Integration test that will test whether reacts are working correctly
    '''

    john = auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')

    john_channel = channels.channels_create(
        john['token'], 'john_channel', True)
    
    old_message = "React to my message"
    message_sent_john = message.message_send(
        john['token'], john_channel['channel_id'], old_message)

    assert message.message_react(john['token'], message_sent_john['message_id'], 1) == {}
    
    with pytest.raises(InputError) as e:
        message.message_react(john['token'], message_sent_john['message_id'], 1)

    assert str(e.value) == '400 Bad Request: Message already contains an active react with react_id'

    assert message.message_unreact(john['token'], message_sent_john['message_id'], 1) == {}
    
    with pytest.raises(InputError) as e:
        message.message_unreact(john['token'], message_sent_john['message_id'], 1)

    assert str(e.value) == '400 Bad Request: Message already does not contain an active react with react_id'
    
    other.clear()



def test_pin_invalid_message():
    '''
    Tests that error is thrown then message_id is not within channel
    BOTH FOR PIN AND UNPIN
    '''

    john = auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')

    channels.channels_create(
        john['token'], 'john_channel', True)

    with pytest.raises(InputError) as e:
        message.message_pin(john['token'], 9999999)

    assert str(e.value) == '400 Bad Request: Message_id is not a valid message'
    
    with pytest.raises(InputError) as e:
        message.message_unpin(john['token'], 9999999)

    assert str(e.value) == '400 Bad Request: Message_id is not a valid message'

    other.clear()


def test_pin_invalid_user():
    '''
    Tests that error is thrown then user is not within channel
    BOTH FOR PIN AND UNPIN
    '''

    john = auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')

    john_channel = channels.channels_create(
        john['token'], 'john_channel', True)

    bob = auth.auth_register(
        'bob@gmail.com', 'qwe123!@#', 'Bob', 'Brown')

    msg = "Try to pin this bob"
    message_sent_john = message.message_send(
        john['token'], john_channel['channel_id'], msg)

    with pytest.raises(AccessError) as e:
        message.message_pin(bob['token'], message_sent_john['message_id'])

    assert str(e.value) == '400 Bad Request: The authorised user is not a member/owner of the channel'
    
    with pytest.raises(AccessError) as e:
        message.message_unpin(bob['token'], message_sent_john['message_id'])

    assert str(e.value) == '400 Bad Request: The authorised user is not a member/owner of the channel'

    other.clear()



def test_pin():
    '''
    Integration test that will test whether pin is working correctly
    '''

    john = auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')

    john_channel = channels.channels_create(
        john['token'], 'john_channel', True)
    
    msg = "Pin this message"
    message_sent_john = message.message_send(
        john['token'], john_channel['channel_id'], msg)

    assert message.message_pin(john['token'], message_sent_john['message_id']) == {}

    with pytest.raises(InputError) as e:
        message.message_pin(john['token'], message_sent_john['message_id'])
    
    assert str(e.value) == '400 Bad Request: Message is already pinned'

    assert message.message_unpin(john['token'], message_sent_john['message_id']) == {}

    with pytest.raises(InputError) as e:
        message.message_unpin(john['token'], message_sent_john['message_id'])

    assert str(e.value) == '400 Bad Request: Message is already unpinned'

    other.clear()


def test_message_send_multiple():
    '''
    Test that messages are being sent and assigned m_id's correctly
    '''

    john = auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    
    john_channel = channels.channels_create(
        john['token'], 'john_channel', True)
    
    message_1 = message.message_send(john['token'], john_channel['channel_id'], "hello")

    assert message_1['message_id'] == 0

    message_2 = message.message_send(john['token'], john_channel['channel_id'], "hello")

    assert message_2['message_id'] == message_1['message_id'] + 1

    other.clear()


def test_message_send_later_inputerrors():
    '''
    Check errors are thrown correctly for message_sendlater
    '''

    john = auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')

    with pytest.raises(InputError) as e:
        message.message_sendlater(john['token'], 88888888, "incorrect channel id", datetime.now())
    
    assert str(e.value) == '400 Bad Request: Invalid channel'

    long_message = """Lorem ipsum dolor sit amet, consectetur adipiscing elit,
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
    nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
    reprehenderit in voluptate velit esse cillum dolore eu fugiat 
    nulla pariatur. Excepteur sint occaecat cupidatat non proident, 
    sunt in culpa qui officia deserunt mollit anim id est laborum.
    Sed ut perspiciatis unde omnis iste natus error sit voluptatem 
    accusantium doloremque laudantium, totam rem aperiam, eaque ipsa 
    quae ab illo inventore veritatis et quasi architecto beatae vitae 
    dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit 
    aspernatur aut odit aut fugit, sed quia consequuntur magni dolores 
    eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, 
    qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, 
    sed quia non numquam eius modi tempora incidunt ut labore et dolore 
    magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis 
    nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut 
    aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit 
    qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum 
    qui dolorem eum fugiat quo voluptas nulla pariatur?"""
    
    timestamp = (datetime.now() + timedelta(days=4)).timestamp()
    
    john_channel = channels.channels_create(john['token'], 'john_channel', True)
    
    with pytest.raises(InputError) as e:
        message.message_sendlater(john['token'], john_channel['channel_id'], long_message, timestamp)
    
    assert str(e.value) == '400 Bad Request: Message is more than 1000 characters'
    
    other.clear()


def test_message_sendlater_multiple():
    '''
    Test that messages are being sent and assigned m_id's correctly
    '''

    john = auth.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    
    john_channel = channels.channels_create(
        john['token'], 'john_channel', True)
    timestamp = (datetime.now() + timedelta(days=4)).timestamp()
    message_1 = message.message_sendlater(john['token'], john_channel['channel_id'], "hello", timestamp)

    assert message_1['message_id'] == 0

    message_2 = message.message_sendlater(john['token'], john_channel['channel_id'], "hello", timestamp)

    assert message_2['message_id'] == message_1['message_id'] + 1

    other.clear()


def test_token_auth():
    '''
    Tests that Access error is throw back for all message functions if incorrect
    token passed
    '''

    with pytest.raises(AccessError) as e:
        message.message_send(invalid_token, 555, "message")
    
    assert str(e.value) == '400 Bad Request: Invalid token'

    with pytest.raises(AccessError) as e:
        message.message_remove(invalid_token, 555)
    
    assert str(e.value) == '400 Bad Request: Invalid token'

    with pytest.raises(AccessError) as e:
        message.message_edit(invalid_token, 555, "message")
    
    assert str(e.value) == '400 Bad Request: Invalid token'

    with pytest.raises(AccessError) as e:
        message.message_sendlater(invalid_token, 555, "message", datetime.now())
    
    assert str(e.value) == '400 Bad Request: Invalid token'

    with pytest.raises(AccessError) as e:
        message.message_react(invalid_token, 555, 999)
    
    assert str(e.value) == '400 Bad Request: Invalid token'

    with pytest.raises(AccessError) as e:
        message.message_unreact(invalid_token, 555, 999)
    
    assert str(e.value) == '400 Bad Request: Invalid token'

    with pytest.raises(AccessError) as e:
        message.message_pin(invalid_token, 555)
    
    assert str(e.value) == '400 Bad Request: Invalid token'

    with pytest.raises(AccessError) as e:
        message.message_unpin(invalid_token, 555)
    
    assert str(e.value) == '400 Bad Request: Invalid token'

    other.clear()

