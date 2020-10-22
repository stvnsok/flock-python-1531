'''
Tests for message.py
'''

import pytest
import re
import auth
import message
import channels
import channel
from error import InputError, AccessError
from other import clear
from data import data
import helper_test_functions as test_setup
from subprocess import Popen, PIPE
import signal
from time import sleep
import pytest


@pytest.fixture
def url():
    '''
    Fixture to get the URL of server
    '''
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")


def test_message_send_length(url):
    '''
    Throws an InputError if they message is longer than 1000 characters
    '''
    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)
    john_channel = test_setup.channels_create(
        john['token'], 'john_channel', True, url)

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

        test_setup.message_send(
            john['token'], john_channel['channel_id'], long_message, url)

    assert str(err.value) == "Message is more than 1000 characters"
    clear()


def test_message_send_unauthorised_user(url):
    '''
    Throws an access error if a user that has not joined the channel tries to post a message
    '''
    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)
    bob = test_setup.auth_register(
        'bob@gmail.com', 'abc123!@#', 'Bob', 'Lime', url)

    bob_channel = test_setup.channels_create(
        bob['token'], 'bob_channel', True, url)

    with pytest.raises(AccessError) as err:
        impossible_message = "I dont think I belong here"
        test_setup.message_send(
            john['token'], bob_channel['channel_id'], impossible_message, url)

    assert str(err.value) == "Authorised user has not joined this channel yet"
    clear()


def test_message_send_sent(url):
    '''
    Tests whether a valid message is stored correctly
    '''
    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)
    john_channel = test_setup.channels_create(
        john['token'], 'john_channel', True, url)
    valid_message = "Hello"
    message_sent_john = test_setup.message_send(
        john['token'], john_channel['channel_id'], valid_message, url)

    assert message_sent_john['message_id'] == valid_message
    clear()


def test_message_remove_invalid_id(url):
    '''
    Throws an Input error if the message based on ID no longer exists
    '''
    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)

    with pytest.raises(InputError) as err:
        message.message_remove(john['token'], 9999)

    assert str(err.value) == "Message does not exist"
    clear()


def test_message_remove_incorrect_user(url):
    '''
    Throws an AccessError if the message id does not map to a message sent by the authorised user
    '''
    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)
    bob = test_setup.auth_register(
        'bob@gmail.com', 'abc123!@#', 'Bob', 'Lime', url)

    bob_channel = test_setup.channels_create(
        bob['token'], 'bob_channel', True, url)
    test_setup.channel_addowner(
        bob['token'], bob_channel['channel_id'], bob['u_id'], url)

    message_sent = test_setup.message_send(
        bob['token'], bob_channel['channel_id'], "Hello", url)

    with pytest.raises(AccessError) as err:
        test_setup.message_remove(
            john['token'], message_sent['message_id'], url)

    assert str(err.value) == "Message to remove was not sent by authorised user"
    clear()


def test_message_remove_unauthorised_user():
    '''
    Throws an AccessError if the user trying to remove a given message
    is not an owner of the corresponding channel
    '''
    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)
    bob = test_setup.auth_register(
        'bob@gmail.com', 'abc123!@#', 'Bob', 'Lime', url)

    bob_channel = test_setup.channels_create(
        bob['token'], 'bob_channel', True, url)

    message_sent = test_setup.message_send(
        bob['token'], bob_channel['channel_id'], "Hello", url)

    with pytest.raises(AccessError) as err:
        test_setup.message_remove(
            john['token'], message_sent['message_id'], url)

    assert str(
        err.value) == "Message to remove was not sent by an owner of this channel"
    clear()


def test_message_remove_removed(url):
    '''
    Test that message was sent and remove successfully
    '''
    bob = test_setup.auth_register(
        'bob@gmail.com', 'abc123!@#', 'Bob', 'Lime', url)

    bob_channel = test_setup.channels_create(
        bob['token'], 'bob_channel', True, url)

    message_sent = test_setup.message_send(
        bob['token'], bob_channel['channel_id'], "Hello", url)

    test_setup.message_remove(bob['token'], message_sent['message_id'], url)
    clear()


def test_message_edit_incorrect_user(url):
    '''
    Throws an AccessError if the message id does not map to a message sent by the authorised user
    '''
    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)
    bob = test_setup.auth_register(
        'bob@gmail.com', 'abc123!@#', 'Bob', 'Lime', url)

    bob_channel = test_setup.channels_create(
        bob['token'], 'bob_channel', True, url)
    test_setup.channel_addowner(
        bob['token'], bob_channel['channel_id'], bob['u_id'], url)

    message_sent = test_setup.message_send(
        bob['token'], bob_channel['channel_id'], "Hello", url)

    with pytest.raises(AccessError) as err:
        test_setup.message_edit(
            john['token'], message_sent['message_id'], "Goodbye", url)

    assert str(err.value) == "Message to remove was not sent by authorised user"
    clear()


def test_message_edit_unauthorised_user(url):
    '''
    Throws an AccessError if the user trying to edit a given message
    is not part of the corresponding channel
    '''
    john = test_setup.auth_register(
        'john@gmail.com', 'qwe123!@#', 'John', 'Smith', url)
    bob = test_setup.auth_register(
        'bob@gmail.com', 'abc123!@#', 'Bob', 'Lime', url)

    bob_channel = test_setup.channels_create(
        bob['token'], 'bob_channel', True, url)

    message_sent = test_setup.message_send(
        bob['token'], bob_channel['channel_id'], "Hello", url)

    with pytest.raises(AccessError) as err:
        test_setup.message_edit(
            john['token'], message_sent['message_id'], "Goodbye", url)

    assert str(
        err.value) == "Message to remove was not sent by an owner of this channel"
    clear()


def test_message_edit_edited():
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

    new_message = "This is the new message"
    test_setup.message_edit(
        john['token'], message_sent_john['message_id'], new_message, url)

    message_in_data = next(message for message in data['messages']
                           if message['message_id'] == message_sent_john['message_id'])

    assert message_in_data['message'] == new_message
    clear()
