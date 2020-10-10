'''
Tests for message.py

'''

import pytest
import message
from error import InputError, AccessError
from other import clear

def test_message_1():
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    bob = auth.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime')
    john_channel = channels.channels_create(john['token'], 'john_channel', True)
    bob_channel = channels.channels_create(bob['token'], 'bob_channel', True) 

    with pytest.raises(InputError) as e:
        long_message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"
        message.message_send(john['token'], john_channel['channel_id'], long_message)

    assert str(e.value) == 'Message is more than 1000 characters'

    with pytest.raises(AccessError) as e:
        impossible_message = "I dont think I belong here"
        message.message_send(john['token'], bob_channel['channel_id'], impossible_message)

    assert str(e.value) == "Authorised user has not joined this channel yet"

    valid_message = "Hello"
    message_sent_john = message_send(john['token'], john_channel['channel_id'], valid_message)

    assert message_sent_john['message_id'] == valid_message

    
    
