'''
Tests for other.py
20/10/20
'''

from data import data
import helper_test_functions
from fixture import url as _url

def test_users_all(_url):   
    # Register new user
    user = helper_test_functions.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne', _url)
    token = user['token']
    helper_test_functions.auth_register('jacknapier@hotmail.com', 'j0kerr', 'Jack', 'Napier', _url)

    # Check if correct items are returned
    users = helper_test_functions.users_all(token, _url)['users']
    
    assert len(users) == 2
    assert users[0]['name_first'] == 'Bruce'
    assert users[1]['name_first'] == 'Jack'

    helper_test_functions.clear(_url)

def test_admin_userpermission_change(_url):
    # Testing if permission changes are correctly executed
    user = helper_test_functions.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne', _url)
    token = user['token']
    users = helper_test_functions.users_all(token, _url)

    # Check if first user permissions are admin permissions (1)
    assert users['users'][0]['permission_id'] == 1

    # Register new user
    user2 = helper_test_functions.auth_register('jacknapier@hotmail.com', 'j0kerr', 'Jack', 'Napier', _url) 
    token2 = user2['token']
    users = helper_test_functions.users_all(token2, _url)

    # Check if first user permissions are regular permissions (2)
    assert users['users'][1]['permission_id'] == 2

    # Change permissions
    helper_test_functions.change_userpermission(user['token'], user2['u_id'], 1, _url)
    users = helper_test_functions.users_all(token, _url)

    # Check if new permissions are in effect
    assert users['users'][1]['permission_id'] == 1

    helper_test_functions.clear(_url)

def test_admin_userpermission_change_invalid_permission_id(_url):
    # Testing if permission changes catch invalid permission ids
    user = helper_test_functions.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne', _url)
    token = user['token']
    users = helper_test_functions.users_all(token, _url)

    # Check if first user permissions are admin permissions (1)
    assert users['users'][0]['permission_id'] == 1

    # Register new user
    user2 = helper_test_functions.auth_register('jacknapier@hotmail.com', 'j0kerr', 'Jack', 'Napier', _url) 
    token2 = user2['token']
    users = helper_test_functions.users_all(token2, _url)

    # Check if first user permissions are regular permissions (2)
    assert users['users'][1]['permission_id'] == 2

    # Change permissions to failure
    error = helper_test_functions.change_userpermission(user['token'], user2['u_id'], 3, _url)
    assert error['code'] == 400
    assert error['message'] == '<p>Permission_id does not refer to a value permission</p>'

    helper_test_functions.clear(_url)

def test_admin_userpermission_change_invalid_admin(_url):
    # Testing if permission changes catch invalid admins
    user = helper_test_functions.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne', _url)
    token = user['token']
    users = helper_test_functions.users_all(token, _url)

    # Check if first user permissions are admin permissions (1)
    assert users['users'][0]['permission_id'] == 1

    # Register new user
    user2 = helper_test_functions.auth_register('jacknapier@hotmail.com', 'j0kerr', 'Jack', 'Napier', _url) 
    token2 = user2['token']
    users = helper_test_functions.users_all(token2, _url)

    # Check if first user permissions are regular permissions (2)
    assert users['users'][1]['permission_id'] == 2

    # Change permissions to failure
    error = helper_test_functions.change_userpermission(user2['token'], user['u_id'], 1, _url)
    assert error['code'] == 400
    assert error['message'] == '<p>The authorised user is not an admin or owner</p>'

    helper_test_functions.clear(_url)

def test_admin_userpermission_change_invalid_user(_url):
    # Testing if permission changes catch invalid users
    user = helper_test_functions.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne', _url)
    token = user['token']
    users = helper_test_functions.users_all(token, _url)

    # Check if first user permissions are admin permissions (1)
    assert users['users'][0]['permission_id'] == 1

    # Register new user
    user2 = helper_test_functions.auth_register('jacknapier@hotmail.com', 'j0kerr', 'Jack', 'Napier', _url) 
    token2 = user2['token']
    users = helper_test_functions.users_all(token2, _url)

    # Check if first user permissions are regular permissions (2)
    assert users['users'][1]['permission_id'] == 2

    # Change permissions to failure
    error = helper_test_functions.change_userpermission(user['token'], 'bat', 1, _url)
    assert error['code'] == 400
    assert error['message'] == '<p>U_id does not refer to a valid user</p>'

    helper_test_functions.clear(_url)

def test_other_search(_url):
    # Register new user
    user = helper_test_functions.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne', _url)
    
    # Create a new channel
    new_channel = helper_test_functions.channels_create(user['token'], 'channel', True, _url)

    # Create new messages
    helper_test_functions.message_send(user['token'], new_channel['channel_id'], 'hello!', _url)
    helper_test_functions.message_send(user['token'], new_channel['channel_id'], 'Just wanted to say goodbye', _url)
    helper_test_functions.message_send(user['token'], new_channel['channel_id'], 'Just wanted to say hello', _url)

    messages = helper_test_functions.search(user['token'], "hello", _url)

    # Check if correct messages are returned
    assert messages['messages'][0]['message'] == 'hello!'
    assert messages['messages'][1]['message'] == 'Just wanted to say hello'

    helper_test_functions.clear(_url)

def test_other_search_none(_url):
    # Register new user
    user = helper_test_functions.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne', _url)
    
    # Create a new channel
    new_channel = helper_test_functions.channels_create(user['token'], 'channel', True, _url)

    # Create new messages
    helper_test_functions.message_send(user['token'], new_channel['channel_id'], 'hello!', _url)
    helper_test_functions.message_send(user['token'], new_channel['channel_id'], 'Just wanted to say hello', _url)
    helper_test_functions.message_send(user['token'], new_channel['channel_id'], 'Just wanted to say goodbye', _url)

    messages = helper_test_functions.search(user['token'], "batmobile", _url)

    # Check if correct messages are returned
    assert messages['messages'] == []

    helper_test_functions.clear(_url)




