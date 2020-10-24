'''
Tests for user.py

'''
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import pytest
from data import data
import helper_test_functions
from fixture import url as _url

# @pytest.fixture
# def _url():
#     '''
#     Use this fixture to get the URL of the server. It starts the server for you,
#     so you don't need to.
#     '''
#     url_re = re.compile(r' \* Running on ([^ ]*)')
#     server = Popen(["python3", "server.py"], stderr=PIPE, stdout=PIPE)
#     line = server.stderr.readline()
#     local_url = url_re.match(line.decode())
#     if local_url:
#         yield local_url.group(1)
#         # Terminate the server
#         server.send_signal(signal.SIGINT)
#         waited = 0
#         while server.poll() is None and waited < 5:
#             sleep(0.1)
#             waited += 0.1
#         if server.poll() is None:
#             server.kill()
#     else:
#         server.kill()
#         raise Exception("Couldn't get URL from local server")


########################### Tests for user/profile #############################

def test_profile_invalid_user_token(_url):
    '''
    This test uses the feature user/profile with an invalid token. The expected
    outcome is giving an error of 400 saying 'Token is incorrect'.
    '''
    # register first user
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user = response
    u_id = new_user["u_id"]

    # input invalid token into user/profile
    response = helper_test_functions.user_profile("token", u_id, _url)
    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Token is incorrect</p>'

    # clears data
    requests.delete(_url + '/clear')

def test_profile_u_id_not_found(_url):
    '''
    This test uses the feature user/profile with an invalid u_id. The expected
    outcome is giving an error of 400 saying 'No users with the entered u_id was
    found'.
    '''
    # register first user
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user = response
    token = new_user['token']

    #request an invalid u_id
    response = helper_test_functions.user_profile(token, 2, _url)
    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>No users with the entered u_id was found</p>'

    # clears data
    requests.delete(_url + '/clear')

def test_profile_display_correct_info(_url):
    '''
    This test uses the feature user/profile with an valid inputs. The expected
    outcome is an dictonary of u_id, email, first name, last name and handle of
    the user with the inputted u_id.
    '''
    # register first user
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user = response
    u_id = new_user['u_id']
    token = new_user['token']

    # display profile of the caller
    response = helper_test_functions.user_profile(token, u_id, _url)

    profile = response
    assert profile['u_id'] == u_id
    assert profile['email'] == "markowong@hotmail.com"
    assert profile['name_first'] == "marko"
    assert profile['name_last'] == "wong"
    assert profile['handle_str'] == "markowong"

    # register second user
    response = helper_test_functions.auth_register(
        "markowong2@hotmail.com",
        "markowong",
        "marko2",
        "wong2",
        _url
    )
    new_user = response
    u_id = new_user['u_id']

    # display profile of another user called from the first user
    response = helper_test_functions.user_profile(token, u_id, _url)
    profile = response
    assert profile['u_id'] == u_id
    assert profile['email'] == "markowong2@hotmail.com"
    assert profile['name_first'] == "marko2"
    assert profile['name_last'] == "wong2"
    assert profile['handle_str'] == "marko2wong2"

    # clears data
    requests.delete(_url + '/clear')

###################### Tests for user/profile/sethandle ########################

def test_profile_handle_invalid_user_token(_url):
    '''
    This test uses the feature user/profile/sethandle with an invalid token. The
    expected outcome is an error of 400 saying 'Token is incorrect'
    '''
    # input invalid token into user/profile/sethandle
    response = helper_test_functions.user_profile_sethandle('token', "Mr.cool", _url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Token is incorrect</p>'

    # clears data
    requests.delete(_url + '/clear')

def test_profile_handle_too_short(_url):
    '''
    This test uses the feature user/profile/sethandle with an invalid handle that
    is too short. Theexpected outcome is an error of 400 saying 'Handle length
    needs to be between 3 and 20.
    '''
    # register first user
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user = response
    token = new_user['token']

    # input invalid handle into user/profile/sethandle
    response = helper_test_functions.user_profile_sethandle(token, "Mr", _url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Handle length needs to be between 3 and 20</p>'

    # clears data
    requests.delete(_url + '/clear')


def test_profile_handle_too_long(_url):
    '''
    This test uses the feature user/profile/sethandle with an invalid handle that
    is too long. The expected outcome is an error of 400 saying 'Handle length
    needs to be between 3 and 20.
    '''
    # register first user
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user = response
    token = new_user['token']

    # input invalid handle into user/profile/sethandle
    response = helper_test_functions.user_profile_sethandle(
        token,
        "soo...how is your day",
        _url
    )

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Handle length needs to be between 3 and 20</p>'

    # clears data
    requests.delete(_url + '/clear')

def test_profile_handle_exisiting(_url):
    '''
    This test uses the feature user/profile/sethandle with an duplicate handle.
    The expected outcome is an error of 400 saying 'Handle already in use by
    another user.
    '''
    # register first user
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user = response
    u_id = new_user['u_id']
    token = new_user['token']

    # input valid handle_str into user/profile
    helper_test_functions.user_profile_sethandle(token, '10/10?', _url)

    for user in data['users']:
        if user['u_id'] == u_id:
            assert user['handle_str'] == "10/10?"

    # register second user
    response = helper_test_functions.auth_register(
        "markowong2@hotmail.com",
        "markowong",
        "marko2",
        "wong2",
        _url
    )
    new_user = response
    u_id = new_user['u_id']
    token = new_user['token']

    # input a valid duplicate handle_str into user/profile
    response = helper_test_functions.user_profile_sethandle(token, '10/10?', _url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Handle already in use by another user</p>'

    # clears data
    requests.delete(_url + '/clear')

def test_profile_handle_correct_update(_url):
    '''
    This test uses the feature user/profile/sethandle with valid inputs. The
    expected outcome is that the handle string stored in the database will change
    to the input handle string.
    '''
    # register first user
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user = response
    u_id = new_user['u_id']
    token = new_user['token']

    # input valid handle_str into user/profile
    helper_test_functions.user_profile_sethandle(token, '10/10?', _url)
    for user in data['users']:
        if user['u_id'] == u_id:
            assert user['handle_str'] == "10/10?"

    # clears data
    requests.delete(_url + '/clear')

###################### Tests for user/profile/setname ##########################

def test_profile_setname_correct_update(_url):
    '''
    This test uses the feature user/profile/setname with valid inputs. The
    expected outcome is the name_first string and name_last string stored in the
    database will change to the inputted strings.
    '''
    # register first user
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user = response
    u_id = new_user['u_id']
    token = new_user['token']

    # input valid name into user/profile/setname
    helper_test_functions.user_profile_setname(
        token,
        "Nikhil",
        "wongsta",
        _url
    )

    for user in data['users']:
        if user['u_id'] == u_id:
            assert user['name_first'] == "Nikhil"
            assert user['name_last'] == "wongsta"

    # clears data
    requests.delete(_url + '/clear')

def test_profile_setname_last_name_too_short(_url):
    '''
    This test uses the feature user/profile/setname with an invalid name_last
    that is too short. The expected outcome is an error of 400 saying 'Handle
    length needs to be between 3 and 20.
    '''
    # register first user
    payload = helper_test_functions.auth_register(
        "brucewayne@hotmail.com",
        "batm4n",
        "bruce",
        "wayne",
        _url
    )
    new_user = payload
    token = new_user['token']

    # call setname function
    response = helper_test_functions.user_profile_setname(token, "Jac", "", _url)

    error = response

    assert error['code'] == 400
    assert error['message'] == '<p>Last name must be between 1 and 50 characters in length</p>'
    requests.delete(_url + '/clear')

def test_profile_setname_last_name_too_long(_url):
    '''
    This test uses the feature user/profile/setname with an invalid name_last
    that is too long. The expected outcome is an error of 400 saying 'Handle
    length needs to be between 3 and 20.
    '''
    # register first user
    payload = helper_test_functions.auth_register(
        "brucewayne@hotmail.com",
        "batm4n",
        "bruce",
        "wayne",
        _url
    )
    new_user = payload
    token = new_user['token']

    # call setname function
    response = helper_test_functions.user_profile_setname(
        token,
        "Jack",
        "is this enough tests yet??? no?... eeeee fine, here's more",
        _url
    )

    error = response

    assert error['code'] == 400
    assert error['message'] == '<p>Last name must be between 1 and 50 characters in length</p>'
    requests.delete(_url + '/clear')

def test_profile_setname_first_name_too_short(_url):
    '''
    This test uses the feature user/profile/setname with an invalid name_first
    that is too short. The expected outcome is an error of 400 saying 'Handle
    length needs to be between 3 and 20.
    '''
    payload = helper_test_functions.auth_register(
        "brucewayne@hotmail.com",
        "batm4n",
        "bruce",
        "wayne",
        _url
    )
    new_user = payload
    token = new_user['token']

    response = helper_test_functions.user_profile_setname(token, "", "Nar", _url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>First name must be between 1 and 50 characters in length</p>'

    requests.delete(_url + '/clear')

def test_profile_setname_first_name_too_long(_url):
    '''
    This test uses the feature user/profile/setname with an invalid name_first
    that is too long. The expected outcome is an error of 400 saying 'Handle
    length needs to be between 3 and 20.
    '''
    payload = helper_test_functions.auth_register(
        "brucewayne@hotmail.com",
        "batm4n",
        "bruce",
        "wayne",
        _url
    )
    new_user = payload
    token = new_user['token']

    response = helper_test_functions.user_profile_setname(
        token,
        "My name is .... I forgot so what is your name? I am very ...",
        "Napier",
        _url
    )

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>First name must be between 1 and 50 characters in length</p>'

    requests.delete(_url + '/clear')


def test_profile_setname_token_incorrect(_url):
    '''
    This test uses the feature user/profile/setname with an invalid token. The
    expected outcome is an error of 400 saying 'Token is incorrect'
    '''
    response = helper_test_functions.user_profile_setname("0", "Jack", "N", _url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Token is incorrect</p>'

    requests.delete(_url + '/clear')

###################### Tests for user/profile/setemail #########################

def test_profile_setemail_not_valid(_url):
    '''
    This test uses the feature user/profile/setemail with an invalid email. The
    expected outcome is an error of 400 saying 'Email is not valid'
    '''
    payload = helper_test_functions.auth_register(
        "brucewayne@hotmail.com",
        "batm4n",
        "bruce",
        "wayne",
        _url
    )
    new_user = payload
    token = new_user['token']

    response = helper_test_functions.user_profile_setemail(
        token,
        "jacknapier.com",
        _url
    )

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Email is not valid</p>'

    requests.delete(_url + '/clear')

def test_set_email_used(_url):

    # Register user
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user = response
    token = new_user['token']

    # Register second user
    response = helper_test_functions.auth_register(
        "markowong2@hotmail.com",
        "markowong2",
        "marko2",
        "wong2",
        _url
    )
    
    response = helper_test_functions.user_profile_setemail(token, "markowong2@hotmail.com", _url)
    
    # Check server response aligns with error messages
    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Email address is already in use</p>'

    requests.delete(_url + '/clear')

def test_profile_setemail_token_incorrect(_url):
    '''
    This test uses the feature user/profile/setemail with an invalid token. The
    expected outcome is an error of 400 saying 'Token is incorrect'
    '''
    response = helper_test_functions.user_profile_setemail('0', "j@hotmail.com", _url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Token is incorrect</p>'

    requests.delete(_url + '/clear')

def test_profile_setemail_correct_update(_url):
    '''
    This test uses the feature user/profile/setemail with valid inputs. The
    expected outcome is the email assoicate the user who calls this function will
    have their email changed in the database.
    '''
    # register first user
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user = response
    u_id = new_user['u_id']
    token = new_user['token']

    # input valid handle_str into user/profile
    helper_test_functions.user_profile_setemail(token, "JayTheCarry@gmail.com", _url)

    for user in data['users']:
        if user['u_id'] == u_id:
            assert user['email'] == "JayTheCarry@gmail.com"

    # clears data
    requests.delete(_url + '/clear')
