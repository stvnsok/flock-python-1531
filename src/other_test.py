from data import data
import auth
import channel
import channels
import message
import other
from error import InputError, AccessError
from datetime import datetime
import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import helper_test_functions
from fixture import url as _url

'''
NEED TO ADD TEST FOR TIMESTAMP
'''
####################################################################################

# @pytest.fixture
# def _url():
#    '''
#    Use this fixture to get the URL of the server. It starts the server for you,
#    so you don't need to.
#    '''
#    url_re = re.compile(r' \* Running on ([^ ]*)')
#    server = Popen(["python3", "server.py"], stderr=PIPE, stdout=PIPE)
#    line = server.stderr.readline()
#    local_url = url_re.match(line.decode())
#    if local_url:
#        yield local_url.group(1)
#        # Terminate the server
#        server.send_signal(signal.SIGINT)
#        waited = 0
#        while server.poll() is None and waited < 5:
#            sleep(0.1)
#            waited += 0.1
#        if server.poll() is None:
#            server.kill()
#    else:
#        server.kill()
#        raise Exception("Couldn't get URL from local server")

#####################################################################################

def test_clear(_url):
    # Create new user
    user = helper_test_functions.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne', _url)
    helper_test_functions.channels_create(user['token'],"channel", True, _url)
    
    other.clear()

    # Check if data structure is empty
    assert len(data['users']) == 0
    assert len(data['channels']) == 0

def test_users_all(_url):   
    # Register new user
    user = helper_test_functions.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne', _url)
    token = user['token']
    helper_test_functions.auth_register('jacknapier@hotmail.com', 'j0kerr', 'Jack', 'Napier', _url)

    # Check if correct items are returned
    assert other.users_all(token) == {'users': data['users']}

    other.clear()


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

    other.clear()


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

    other.clear()

'''
def test_admin_userpermission_change_invalid_admin(_url):
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

def test_admin_userpermission_change_invalid_user(_url):
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

'''
def test_other_search(_url):
    # Register new user
    user = helper_test_functions.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne', _url)
    
    # Create a new channel
    new_channel = helper_test_functions.channels_create(user['token'], 'channel', True, _url)

    # Create new messages
    helper_test_functions.message_send(user['token'], new_channel['channel_id'], 'hello!', _url)
    helper_test_functions.message_send(user['token'], new_channel['channel_id'], 'Just wanted to say hello', _url)
    helper_test_functions.message_send(user['token'], new_channel['channel_id'], 'Just wanted to say goodbye', _url)

    messages = helper_test_functions.search(user['token'], "hello", _url)

    # Check if correct messages are returned
    assert messages['messages'][0]['message'] == 'hello!'
    assert messages['messages'][1]['message'] == 'Just wanted to say hello'

    other.clear()

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

    other.clear()

def test_check_email_false():
    # Test invalid email
    email = 'jacknapier.com'
    assert other.check(email) == False

def test_check_email_true():
    # Test valid email
    email = 'jacknapier@hotmail.com'
    assert other.check(email) == True

