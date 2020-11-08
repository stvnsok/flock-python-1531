'''
Tests for message.py
Written on 15/10/2020
'''

import helper_test_functions as test_setup
from fixture import url
from datetime import datetime, timedelta


def test_message_send_length(url):
    '''
    Throws an InputError if they message is longer than 1000 characters
    '''

    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)
    john_channel = test_setup.channels_create(
        john['token'], 'john_channel', True, url)

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

    error_response = test_setup.message_send(
        john['token'], john_channel['channel_id'], long_message, url)
    
    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Message is more than 1000 characters</p>"

    test_setup.clear(url)


def test_message_uninvited_user(url):
    '''
    Throws an access error if a user that has not joined the channel tries to post a message
    '''
    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)
    bob = test_setup.auth_register(
        'bob@gmail.com', 'abc123!@#', 'Bob', 'Lime', url)

    bob_channel = test_setup.channels_create(
        bob['token'], 'bob_channel', True, url)

    impossible_message = "I dont think I belong here"
       
    error_response = test_setup.message_send(
            john['token'], bob_channel['channel_id'], impossible_message, url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Authorised user has not joined this channel yet</p>"

    
    test_setup.clear(url)


def test_message_send_and_remove(url):
    '''
    Tests whether a valid message is stored correctly and can be removed
    '''
    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)
    john_channel = test_setup.channels_create(
        john['token'], 'john_channel', True, url)
    
    valid_message = "Hello"
    message_sent_john = test_setup.message_send(
        john['token'], john_channel['channel_id'], valid_message, url)

    response = test_setup.message_remove(john['token'], message_sent_john['message_id'], url)

    assert response == {}

    test_setup.clear(url)


def test_message_remove_invalid_id(url):
    '''
    Throws an Input error if the message based on ID no longer exists
    '''
    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)

    error_response =  test_setup.message_remove(john['token'], 9999, url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Message does not exist</p>"

    error_response =  test_setup.message_edit(john['token'], 9999, "Goodbye", url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Message does not exist</p>"
    
    test_setup.clear(url)


def test_message_unauthorised_user(url):
    '''
    Throws an AccessError if the message id does not map to a message 
    sent by the authorised user
    '''
    test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)
    bob = test_setup.auth_register(
        'bob@gmail.com', 'abc123!@#', 'Bob', 'Lime', url)
    sally = test_setup.auth_register(
        'sally@gmail.com', 'Helo123!', 'Sally', 'Lemon', url
    )

    bob_channel = test_setup.channels_create(
        bob['token'], 'bob_channel', True, url)
    test_setup.channel_addowner(
        bob['token'], bob_channel['channel_id'], bob['u_id'], url)
    

    message_sent = test_setup.message_send(
        bob['token'], bob_channel['channel_id'], "Hello", url)

    error_response = test_setup.message_remove(
            sally['token'], message_sent['message_id'], url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Message to remove was not sent by authorised user. Authorised user is not an owner of the channel</p>"

    error_response = test_setup.message_edit(
            sally['token'], message_sent['message_id'], "Goodbye",url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Message to remove was not sent by authorised user. Authorised user is not an owner of the channel</p>"

    test_setup.clear(url)


def test_message_user_permissions(url):
    '''
    Test that John as an owner of Flockr cannot delete/edit messages even though he has global
    permissions because he is not in the channel Bob set up
    '''
    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)
    bob = test_setup.auth_register(
        'bob@gmail.com', 'abc123!@#', 'Bob', 'Lime', url)

    bob_channel = test_setup.channels_create(
        bob['token'], 'bob_channel', True, url)

    message_sent = test_setup.message_send(
        bob['token'], bob_channel['channel_id'], "Hello", url)

    error_response = test_setup.message_remove(
            john['token'], message_sent['message_id'], url)

    assert error_response['code'] == 400
    assert error_response['message'] == "<p>Message to remove was not sent by authorised user. Authorised user is not an owner of the channel</p>"
    
    error_response = test_setup.message_edit(
            john['token'], message_sent['message_id'], "Goodbye", url)

    assert error_response['code'] == 400
    assert error_response['message'] == "<p>Message to remove was not sent by authorised user. Authorised user is not an owner of the channel</p>"

    test_setup.clear(url)



def test_message_edit_edited(url):
    '''
    Test that a message sent can be edited successfully and correctly
    '''
    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)
    john_channel = test_setup.channels_create(
        john['token'], 'john_channel', True, url)

    old_message = "This is the old message"
    message_sent_john = test_setup.message_send(
        john['token'], john_channel['channel_id'], old_message, url)

    message_in_data = test_setup.search(john['token'], "This is the", url) 

    assert message_in_data['messages'][0]['message'] == old_message

    new_message = "This is the new message"
    test_setup.message_edit(
        john['token'], message_sent_john['message_id'], new_message, url)


    message_in_data = test_setup.search(john['token'], "This is the new message", url) 

    assert message_in_data['messages'][0]['message'] == new_message
    test_setup.clear(url)


def test_message_sendlater_invalid_time(url):
    '''
    Test that a message sent with past timestamp throws error
    '''
    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)
    john_channel = test_setup.channels_create(
        john['token'], 'john_channel', True, url)

    future_message = "This is a message from the past"
    future_date = datetime.now() + timedelta(days=-4) 
    future_date = future_date.timestamp()

    error_response = test_setup.message_sendlater(john['token'], john_channel['channel_id'], future_message, future_date,url)

    assert error_response['code'] == 400
    assert error_response['message'] == '<p>Time sent is a time in the past</p>'

    test_setup.clear(url)

def test_message_sendlater_invalid_user(url):
    '''
    Test that a message sent from unauthorised user throws error
    '''
    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)
    bob = test_setup.auth_register(
        'bob@gmail.com', 'qwe123!@#', 'Bob', 'Smith', url)
    john_channel = test_setup.channels_create(
        john['token'], 'john_channel', True, url)

    future_message = "This is a message from the past"
    future_date = datetime.now() + timedelta(days=4) 
    future_date = future_date.timestamp()

    error_response = test_setup.message_sendlater(bob['token'], john_channel['channel_id'], future_message, future_date,url)

    assert error_response['code'] == 400
    assert error_response['message'] == '<p>Authorised user has not joined the channel</p>'

    test_setup.clear(url)

def test_message_sendlater(url):
    '''
    Test that a message sent with past timestamp throws error
    '''
    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)

    john_channel = test_setup.channels_create(
        john['token'], 'john_channel', True, url)

    future_message = "This is a message for the future"
    future_date = datetime.now() + timedelta(days=4) 
    future_date = future_date.timestamp()

    response = test_setup.message_sendlater(john['token'], john_channel['channel_id'], future_message, future_date,url)

    assert response['message_id'] == 0

    test_setup.clear(url)


def test_react_invalid_message(url):
    '''
    Tests that error is thrown then message_id is not within channel
    BOTH FOR REACT AND UNREACT
    '''
    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)

    test_setup.channels_create(
        john['token'], 'john_channel', True, url)

    error_response = test_setup.message_react(john['token'], 9999999, 1, url)

    assert error_response['code'] == 400
    assert error_response['message'] == '<p>Message_id is not a valid message within a channel that the authorised user has joined</p>'


    error_response = test_setup.message_unreact(john['token'], 9999999, 1, url)

    assert error_response['code'] == 400
    assert error_response['message'] == '<p>Message_id is not a valid message within a channel that the authorised user has joined</p>'

    test_setup.clear(url)

def test_react_invalid_react_id(url):
    '''
    Tests that error is thrown when react_id is not correct
    BOTH FOR REACT AND UNREACT
    '''
    
    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)

    test_setup.channels_create(
        john['token'], 'john_channel', True, url)

    error_response = test_setup.message_react(john['token'], 9999999, 100, url)

    assert error_response['code'] == 400
    assert error_response['message'] == '<p>React_id is not a valid React ID</p>'


    error_response = test_setup.message_unreact(john['token'], 9999999, 100, url)

    assert error_response['code'] == 400
    assert error_response['message'] == '<p>React_id is not a valid React ID</p>'

    test_setup.clear(url)

def test_react(url):
    '''
    Integration test that will test whether reacts are working correctly
    '''
    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)

  
    john_channel = test_setup.channels_create(
        john['token'], 'john_channel', True, url)
    
    old_message = "React to my message"
    message_sent_john = test_setup.message_send(
        john['token'], john_channel['channel_id'], old_message, url)

    test_setup.message_react(john['token'], message_sent_john['message_id'], 1, url)
    
    error_response = test_setup.message_react(john['token'], message_sent_john['message_id'], 1, url)

    assert error_response['code'] == 400
    assert error_response['message'] == '<p>Message already contains an active react with react_id</p>'

    test_setup.message_unreact(john['token'], message_sent_john['message_id'], 1, url)
    
    error_response = test_setup.message_unreact(john['token'], message_sent_john['message_id'], 1, url)

    assert error_response['code'] == 400
    assert error_response['message'] == '<p>Message already does not contain an active react with react_id</p>'

    test_setup.clear(url)

def test_pin_invalid_message(url):
    '''
    Tests that error is thrown then message_id is not within channel
    BOTH FOR PIN AND UNPIN
    '''
    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)

    test_setup.channels_create(
        john['token'], 'john_channel', True, url)

    error_response = test_setup.message_pin(john['token'], 9999999, url)

    assert error_response['code'] == 400
    assert error_response['message'] == '<p>Message_id is not a valid message</p>'


    error_response = test_setup.message_unpin(john['token'], 9999999, url)

    assert error_response['code'] == 400
    assert error_response['message'] == '<p>Message_id is not a valid message</p>'

    test_setup.clear(url)

def test_pin_invalid_user(url):
    '''
    Tests that error is thrown then user is not within channel
    BOTH FOR PIN AND UNPIN
    '''
    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)

    john_channel = test_setup.channels_create(
        john['token'], 'john_channel', True, url)

    bob = test_setup.auth_register(
        'bob@gmail.com', 'qwe123!@#', 'Bob', 'Brown', url)

    message = "Try to pin this bob ;)"
    message_sent_john = test_setup.message_send(
        john['token'], john_channel['channel_id'], message, url)

    error_response = test_setup.message_pin(bob['token'], message_sent_john['message_id'], url)

    assert error_response['code'] == 400
    assert error_response['message'] == '<p>The authorised user is not a member/owner of the channel</p>'


    error_response = test_setup.message_unpin(bob['token'], message_sent_john['message_id'], url)

    assert error_response['code'] == 400
    assert error_response['message'] == '<p>The authorised user is not a member/owner of the channel</p>'

    test_setup.clear(url)


def test_pin(url):
    '''
    Integration test that will test whether pin is working correctly
    '''

    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)

    john_channel = test_setup.channels_create(
        john['token'], 'john_channel', True, url)
    
    message = "Pin this message"
    message_sent_john = test_setup.message_send(
        john['token'], john_channel['channel_id'], message, url)

    test_setup.message_pin(john['token'], message_sent_john['message_id'], url)

    error_response = test_setup.message_pin(john['token'], message_sent_john['message_id'], url)

    assert error_response['code'] == 400
    assert error_response['message'] == '<p>Message is already pinned</p>'

    test_setup.message_unpin(john['token'], message_sent_john['message_id'], url)

    error_response = test_setup.message_unpin(john['token'], message_sent_john['message_id'], url)

    assert error_response['code'] == 400
    assert error_response['message'] == '<p>Message is already unpinned</p>'

    test_setup.clear(url)
