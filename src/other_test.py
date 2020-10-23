from data import data
import auth
import channel
import channels
import message
import other
from error import InputError, AccessError
from datetime import datetime
import pytest
'''
NEED TO ADD TEST FOR TIMESTAMP
'''
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


def test_admin_userpermission_change():
    # Testing if permission changes are correctly executed
    user = auth.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne')
    users = data['users']
    token = user['token']
    
    authorised_user = next((user for user in users if user['token'] == token), None)
    assert authorised_user['permission_id'] == 1

    user2 = auth.auth_register('jacknapier@hotmail.com', 'j0kerr', 'Jack', 'Napier') 
    token2 = user2['token']

    authorised_user2 = next((user for user in users if user['token'] == token2), None)
    assert authorised_user2['permission_id'] == 2

    other.admin_userpermission_change(user['token'], user2['u_id'], 1)
    assert authorised_user2['permission_id'] == 1

    other.clear()

def test_admin_userpermission_change_invalid_permission_id():
    # Testing if permission changes catch invalid permission ids
    user = auth.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne')
    users = data['users']
    token = user['token']
    
    authorised_user = next((user for user in users if user['token'] == token), None)
    assert authorised_user['permission_id'] == 1

    user2 = auth.auth_register('jacknapier@hotmail.com', 'j0kerr', 'Jack', 'Napier') 
    token2 = user2['token']

    authorised_user2 = next((user for user in users if user['token'] == token2), None)
    assert authorised_user2['permission_id'] == 2
    
    with pytest.raises(InputError) as e:
        other.admin_userpermission_change(user['token'], user2['u_id'], 3)
    assert '400 Bad Request: Permission_id does not refer to a value permission' == str(e.value)

    other.clear()

def test_admin_userpermission_change_invalid_admin():
    # Testing if permission changes catch invalid admins
    user = auth.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne')
    users = data['users']
    token = user['token']
    
    authorised_user = next((user for user in users if user['token'] == token), None)
    assert authorised_user['permission_id'] == 1

    user2 = auth.auth_register('jacknapier@hotmail.com', 'j0kerr', 'Jack', 'Napier') 
    token2 = user2['token']

    authorised_user2 = next((user for user in users if user['token'] == token2), None)
    assert authorised_user2['permission_id'] == 2
    
    with pytest.raises(InputError) as e:
        other.admin_userpermission_change(user2['token'], user['u_id'], 2)
    assert '400 Bad Request: The authorised user is not an admin or owner' == str(e.value)

    other.clear()

def test_admin_userpermission_change_invalid_user():
    # Testing if permission changes catch invalid users
    user = auth.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne')
    users = data['users']
    token = user['token']
    
    authorised_user = next((user for user in users if user['token'] == token), None)
    assert authorised_user['permission_id'] == 1

    user2 = auth.auth_register('jacknapier@hotmail.com', 'j0kerr', 'Jack', 'Napier') 
    token2 = user2['token']

    authorised_user2 = next((user for user in users if user['token'] == token2), None)
    assert authorised_user2['permission_id'] == 2
    
    with pytest.raises(InputError) as e:
        other.admin_userpermission_change(user['token'], 'bat', 2)
    assert '400 Bad Request: U_id does not refer to a valid user' == str(e.value)

    other.clear()

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
    other.clear()

def test_other_search_none():
    # Register new user
    user = auth.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne')
    
    # Create a new channel
    new_channel = channels.channels_create(user['token'], 'channel', True)

    # Create new messages
    message.message_send(user['token'], new_channel['channel_id'], 'hello!')
    message.message_send(user['token'], new_channel['channel_id'], 'Just wanted to say hello')
    message.message_send(user['token'], new_channel['channel_id'], 'Just wanted to say goodbye')

    messages = other.search(user['token'], "batmobile")

    # Check if correct messages are returned
    assert messages == {'messages': []}
    other.clear()

def test_check_email_false():
    # Test invalid email
    email = 'jacknapier.com'
    assert other.check(email) == False

def test_check_email_true():
    # Test valid email
    email = 'jacknapier@hotmail.com'
    assert other.check(email) == True

 