from data import data
import auth
import channel
import channels
import message
import other
from error import InputError, AccessError
from datetime import datetime

def test_clear():
    # Create new user
    user = auth.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne')
    channels.channels_create(user['token'],"channel", True)
    
    other.clear()

    # Check if data structure is empty
    assert len(data['users']) == 0
    assert len(data['channels']) == 0

def test_users_all():   
    # Register new user
    user = auth.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne')
    token = user['token']
    auth.auth_register('jacknapier@hotmail.com', 'j0kerr', 'Jack', 'Napier')

    # Check if correct items are returned
    assert other.users_all(token) == {'users': data['users']}

    other.clear()

'''
def test_admin_userpermission_change():

    user = auth.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne')
    assert user['permission_id'] == 1

    user2 = auth.auth_register('jacknapier@hotmail.com', 'j0kerr', 'Jack', 'Napier')
    other.admin_userpermission_change(user['token'], user2['u_id'], 1)
   
    assert user2['permission_id'] == 1
'''

def test_other_search():
    # Register new user
    user = auth.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne')
    
    # Create a new channel
    new_channel = channels.channels_create(user['token'], 'channel', True)

    # Create new messages
    message.message_send(user['token'], new_channel['channel_id'], 'hello!')
    message.message_send(user['token'], new_channel['channel_id'], 'Just wanted to say hello')
    message.message_send(user['token'], new_channel['channel_id'], 'Just wanted to say goodbye')

    messages = other.search(user['token'], "hello")

    # Check if correct messages are returned
    assert messages == {'messages': ['hello!', 'Just wanted to say hello']}


