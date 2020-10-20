'''
Tests for message.py

'''

import pytest
import auth
import message
import channels
import channel
from error import InputError, AccessError
from other import clear
from data import data


def test_message_send_length():
    '''
    Throws an InputError if they message is longer than 1000 characters
    '''
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    john_channel = channels.channels_create(
        john['token'], 'john_channel', True)

    with pytest.raises(InputError) as err:
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

        message.message_send(
            john['token'], john_channel['channel_id'], long_message)

    assert str(err.value) == "Message is more than 1000 characters"
    clear()


def test_message_send_unauthorised_user():
    '''
    Throws an access error if a user that has not joined the channel tries to post a message
    '''
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    bob = auth.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime')

    bob_channel = channels.channels_create(bob['token'], 'bob_channel', True)

    with pytest.raises(AccessError) as err:
        impossible_message = "I dont think I belong here"
        message.message_send(
            john['token'], bob_channel['channel_id'], impossible_message)

    assert str(err.value) == "Authorised user has not joined this channel yet"
    clear()


def test_message_send_sent():
    '''
    Tests whether a valid message is stored correctly
    '''
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    john_channel = channels.channels_create(
        john['token'], 'john_channel', True)
    valid_message = "Hello"
    message_sent_john = message.message_send(
        john['token'], john_channel['channel_id'], valid_message)

    assert message_sent_john['message_id'] == valid_message
    clear()


def test_message_remove_invalid_id():
    '''
    Throws an Input error if the message based on ID no longer exists
    '''
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')

    with pytest.raises(InputError) as err:
        message.message_remove(john['token'], 9999)

    assert str(err.value) == "Message does not exist"
    clear()


def test_message_remove_incorrect_user():
    '''
    Throws an AccessError if the message id does not map to a message sent by the authorised user
    '''
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    bob = auth.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime')

    bob_channel = channels.channels_create(bob['token'], 'bob_channel', True)
    channel.channel_addowner(
        bob['token'], bob_channel['channel_id'], bob['u_id'])

    message_sent = message.message_send(
        bob['token'], bob_channel['channel_id'], "Hello")

    with pytest.raises(AccessError) as err:
        message.message_remove(john['token'], message_sent['message_id'])

    assert str(err.value) == "Message to remove was not sent by authorised user"
    clear()


def test_message_remove_unauthorised_user():
    '''
    Throws an AccessError if the user trying to remove a given message
    is not an owner of the corresponding channel
    '''
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    bob = auth.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime')

    bob_channel = channels.channels_create(bob['token'], 'bob_channel', True)

    message_sent = message.message_send(
        bob['token'], bob_channel['channel_id'], "Hello")

    with pytest.raises(AccessError) as err:
        message.message_remove(john['token'], message_sent['message_id'])

    assert str(
        err.value) == "Message to remove was not sent by an owner of this channel"
    clear()


def test_message_remove_removed():
    '''
    Test that message was sent and remove successfully
    '''
    bob = auth.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime')

    bob_channel = channels.channels_create(bob['token'], 'bob_channel', True)

    message_sent = message.message_send(
        bob['token'], bob_channel['channel_id'], "Hello")

    message.message_remove(bob['token'], message_sent['message_id'])
    clear()


def test_message_edit_incorrect_user():
    '''
    Throws an AccessError if the message id does not map to a message sent by the authorised user
    '''
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    bob = auth.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime')

    bob_channel = channels.channels_create(bob['token'], 'bob_channel', True)
    channel.channel_addowner(
        bob['token'], bob_channel['channel_id'], bob['u_id'])

    message_sent = message.message_send(
        bob['token'], bob_channel['channel_id'], "Hello")

    with pytest.raises(AccessError) as err:
        message.message_edit(
            john['token'], message_sent['message_id'], "Goodbye")

    assert str(err.value) == "Message to remove was not sent by authorised user"
    clear()


def test_message_edit_unauthorised_user():
    '''
    Throws an AccessError if the user trying to edit a given message
    is not part of the corresponding channel
    '''
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    bob = auth.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime')

    bob_channel = channels.channels_create(bob['token'], 'bob_channel', True)

    message_sent = message.message_send(
        bob['token'], bob_channel['channel_id'], "Hello")

    with pytest.raises(AccessError) as err:
        message.message_edit(
            john['token'], message_sent['message_id'], "Goodbye")

    assert str(
        err.value) == "Message to remove was not sent by an owner of this channel"
    clear()


def test_message_edit_edited():
    '''
    Test that a message sent can be edited successfully and correctly
    '''
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    john_channel = channels.channels_create(
        john['token'], 'john_channel', True)

    old_message = "This is the old message"
    message_sent_john = message.message_send(
        john['token'], john_channel['channel_id'], old_message)

    new_message = "This is the new message"
    message.message_edit(
        john['token'], message_sent_john['message_id'], new_message)

    message_in_data = next(message for message in data['messages']
                           if message['message_id'] == message_sent_john['message_id'])

    assert message_in_data['message'] == new_message
    clear()
