'''
Tests for other.py
20/10/20
'''
import pytest
from data import data
import auth
import channels
import channel
import other
import message
from error import AccessError, InputError
import helper_test_functions

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
    users = other.users_all(token)['users']
    
    assert len(users) == 2
    assert users[0]['name_first'] == 'Bruce'
    assert users[1]['name_first'] == 'Jack'

    other.clear()

def test_admin_userpermission_change():
    # Testing if permission changes are correctly executed
    user = auth.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne')
    token = user['token']
    users = other.users_all(token)

    # Check if first user permissions are admin permissions (1)
    assert users['users'][0]['permission_id'] == 1

    # Register new user
    user2 = auth.auth_register('jacknapier@hotmail.com', 'j0kerr', 'Jack', 'Napier') 
    token2 = user2['token']
    users = other.users_all(token2)

    # Check if first user permissions are regular permissions (2)
    assert users['users'][1]['permission_id'] == 2

    # Change permissions
    other.admin_userpermission_change(user['token'], user2['u_id'], 1)
    users = other.users_all(token)

    # Check if new permissions are in effect
    assert users['users'][1]['permission_id'] == 1

    other.clear()

def test_admin_userpermission_change_invalid_permission_id():
    # Testing if permission changes catch invalid permission ids
    user = auth.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne')
    token = user['token']
    users = other.users_all(token)

    # Check if first user permissions are admin permissions (1)
    assert users['users'][0]['permission_id'] == 1

    # Register new user
    user2 = auth.auth_register('jacknapier@hotmail.com', 'j0kerr', 'Jack', 'Napier') 
    token2 = user2['token']
    users = other.users_all(token2)

    # Check if first user permissions are regular permissions (2)
    assert users['users'][1]['permission_id'] == 2

    # Change permissions to failure
    with pytest.raises(InputError) as e:
        other.admin_userpermission_change(user['token'], user2['u_id'], 3)
    
    assert str(e.value) == '400 Bad Request: Permission_id does not refer to a value permission'
   

    other.clear()

def test_admin_userpermission_change_invalid_admin():
    # Testing if permission changes catch invalid admins
    user = auth.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne')
    token = user['token']
    users = other.users_all(token)

    # Check if first user permissions are admin permissions (1)
    assert users['users'][0]['permission_id'] == 1

    # Register new user
    user2 = auth.auth_register('jacknapier@hotmail.com', 'j0kerr', 'Jack', 'Napier') 
    token2 = user2['token']
    users = other.users_all(token2)

    # Check if first user permissions are regular permissions (2)
    assert users['users'][1]['permission_id'] == 2

    # Change permissions to failure
    with pytest.raises(InputError) as e:
        other.admin_userpermission_change(user2['token'], user['u_id'], 1)
    
    assert str(e.value) == '400 Bad Request: The authorised user is not an admin or owner'
 
    other.clear()

def test_admin_userpermission_change_invalid_user():
    # Testing if permission changes catch invalid users
    user = auth.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne')
    token = user['token']
    users = other.users_all(token)

    # Check if first user permissions are admin permissions (1)
    assert users['users'][0]['permission_id'] == 1

    # Register new user
    user2 = auth.auth_register('jacknapier@hotmail.com', 'j0kerr', 'Jack', 'Napier') 
    token2 = user2['token']
    users = other.users_all(token2)

    # Check if first user permissions are regular permissions (2)
    assert users['users'][1]['permission_id'] == 2

    # Change permissions to failure
    with pytest.raises(InputError) as e:
        other.admin_userpermission_change(user['token'], 'bat', 1)
    
    assert str(e.value) == '400 Bad Request: U_id does not refer to a valid user'
   
    other.clear()

def test_other_search():
    # Register new user
    user = auth.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne')
    
    # Create a new channel
    new_channel = channels.channels_create(user['token'], 'channel', True)

    # Create new messages
    message.message_send(user['token'], new_channel['channel_id'], 'hello!')
    message.message_send(user['token'], new_channel['channel_id'], 'Just wanted to say goodbye')
    message.message_send(user['token'], new_channel['channel_id'], 'Just wanted to say hello')

    messages = other.search(user['token'], "hello")

    # Check if correct messages are returned
    assert messages['messages'][0]['message'] == 'hello!'
    assert messages['messages'][1]['message'] == 'Just wanted to say hello'

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
    assert messages['messages'] == []

    other.clear()
