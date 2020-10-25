'''
Tests for user.py
'''

import helper_test_functions
from fixture import url

########################### Tests for user/profile #############################

def test_profile_invalid_user_token(url):
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
        url
    )
    new_user = response
    u_id = new_user["u_id"]

    # input invalid token into user/profile
    response = helper_test_functions.user_profile("token", u_id, url)
    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Token is incorrect</p>'

    # clears data
    helper_test_functions.clear(url)

def test_profile_u_id_not_found(url):
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
        url
    )
    new_user = response
    token = new_user['token']

    #request an invalid u_id
    response = helper_test_functions.user_profile(token, 2, url)
    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>No users with the entered u_id was found</p>'

    # clears data
    helper_test_functions.clear(url)

def test_profile_display_correct_info(url):
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
        url
    )
    new_user = response
    u_id = new_user['u_id']
    token = new_user['token']

    # display profile of the caller
    response = helper_test_functions.user_profile(token, u_id, url)

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
        url
    )
    new_user = response
    u_id = new_user['u_id']

    # display profile of another user called from the first user
    response = helper_test_functions.user_profile(token, u_id, url)
    profile = response
    assert profile['u_id'] == u_id
    assert profile['email'] == "markowong2@hotmail.com"
    assert profile['name_first'] == "marko2"
    assert profile['name_last'] == "wong2"
    assert profile['handle_str'] == "marko2wong2"

    # clears data
    helper_test_functions.clear(url)

###################### Tests for user/profile/sethandle ########################

def test_profile_handle_invalid_user_token(url):
    '''
    This test uses the feature user/profile/sethandle with an invalid token. The
    expected outcome is an error of 400 saying 'Token is incorrect'
    '''
    # input invalid token into user/profile/sethandle
    response = helper_test_functions.user_profile_sethandle('token', "Mr.cool", url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Token is incorrect</p>'

    # clears data
    helper_test_functions.clear(url)

def test_profile_handle_too_short(url):
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
        url
    )
    new_user = response
    token = new_user['token']

    # input invalid handle into user/profile/sethandle
    response = helper_test_functions.user_profile_sethandle(token, "Mr", url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Handle length needs to be between 3 and 20</p>'

    # clears data
    helper_test_functions.clear(url)


def test_profile_handle_too_long(url):
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
        url
    )
    new_user = response
    token = new_user['token']

    # input invalid handle into user/profile/sethandle
    response = helper_test_functions.user_profile_sethandle(
        token,
        "soo...how is your day",
        url
    )

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Handle length needs to be between 3 and 20</p>'

    # clears data
    helper_test_functions.clear(url)

def test_profile_handle_exisiting(url):
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
        url
    )
    new_user = response
    u_id = new_user['u_id']
    token = new_user['token']

    # input valid handle_str into user/profile
    helper_test_functions.user_profile_sethandle(token, '10/10?', url)

    users = helper_test_functions.users_all(token, url)

    for user in users['users']:
        if user['u_id'] == u_id:
            assert user['handle_str'] == "10/10?"

    # register second user
    response = helper_test_functions.auth_register(
        "markowong2@hotmail.com",
        "markowong",
        "marko2",
        "wong2",
        url
    )
    new_user = response
    u_id = new_user['u_id']
    token = new_user['token']

    # input a valid duplicate handle_str into user/profile
    response = helper_test_functions.user_profile_sethandle(token, '10/10?', url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Handle already in use by another user</p>'

    # clears data
    helper_test_functions.clear(url)

def test_profile_handle_correct_update(url):
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
        url
    )
    new_user = response
    u_id = new_user['u_id']
    token = new_user['token']

    # input valid handle_str into user/profile
    helper_test_functions.user_profile_sethandle(token, '10/10?', url)

    users = helper_test_functions.users_all(token, url)

    for user in users['users']:
        if user['u_id'] == u_id:
            assert user['handle_str'] == "10/10?"

    # clears data
    helper_test_functions.clear(url)

###################### Tests for user/profile/setname ##########################

def test_profile_setname_correct_update(url):
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
        url
    )
    new_user = response
    u_id = new_user['u_id']
    token = new_user['token']

    # input valid name into user/profile/setname
    helper_test_functions.user_profile_setname(
        token,
        "Nikhil",
        "wongsta",
        url
    )

    users = helper_test_functions.users_all(token, url)

    for user in users['users']:
        if user['u_id'] == u_id:
            assert user['name_first'] == "Nikhil"
            assert user['name_last'] == "wongsta"

    # clears data
    helper_test_functions.clear(url)

def test_profile_setname_last_name_too_short(url):
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
        url
    )
    new_user = payload
    token = new_user['token']

    # call setname function
    response = helper_test_functions.user_profile_setname(token, "Jac", "", url)

    error = response

    assert error['code'] == 400
    assert error['message'] == '<p>Last name must be between 1 and 50 characters in length</p>'
    helper_test_functions.clear(url)

def test_profile_setname_last_name_too_long(url):
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
        url
    )
    new_user = payload
    token = new_user['token']

    # call setname function
    response = helper_test_functions.user_profile_setname(
        token,
        "Jack",
        "is this enough tests yet??? no?... eeeee fine, here's more",
        url
    )

    error = response

    assert error['code'] == 400
    assert error['message'] == '<p>Last name must be between 1 and 50 characters in length</p>'
    helper_test_functions.clear(url)

def test_profile_setname_first_name_too_short(url):
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
        url
    )
    new_user = payload
    token = new_user['token']

    response = helper_test_functions.user_profile_setname(token, "", "Nar", url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>First name must be between 1 and 50 characters in length</p>'

    helper_test_functions.clear(url)

def test_profile_setname_first_name_too_long(url):
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
        url
    )
    new_user = payload
    token = new_user['token']

    response = helper_test_functions.user_profile_setname(
        token,
        "My name is .... I forgot so what is your name? I am very ...",
        "Napier",
        url
    )

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>First name must be between 1 and 50 characters in length</p>'

    helper_test_functions.clear(url)


def test_profile_setname_token_incorrect(url):
    '''
    This test uses the feature user/profile/setname with an invalid token. The
    expected outcome is an error of 400 saying 'Token is incorrect'
    '''
    response = helper_test_functions.user_profile_setname("0", "Jack", "N", url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Token is incorrect</p>'

    helper_test_functions.clear(url)

###################### Tests for user/profile/setemail #########################

def test_profile_setemail_not_valid(url):
    '''
    This test uses the feature user/profile/setemail with an invalid email. The
    expected outcome is an error of 400 saying 'Email is not valid'
    '''
    payload = helper_test_functions.auth_register(
        "brucewayne@hotmail.com",
        "batm4n",
        "bruce",
        "wayne",
        url
    )
    new_user = payload
    token = new_user['token']

    response = helper_test_functions.user_profile_setemail(
        token,
        "jacknapier.com",
        url
    )

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Email is not valid</p>'

    helper_test_functions.clear(url)

def test_set_email_used(url):

    # Register user
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        url
    )
    new_user = response
    token = new_user['token']

    # Register second user
    response = helper_test_functions.auth_register(
        "markowong2@hotmail.com",
        "markowong2",
        "marko2",
        "wong2",
        url
    )
    
    response = helper_test_functions.user_profile_setemail(token, "markowong2@hotmail.com", url)
    
    # Check server response aligns with error messages
    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Email address is already in use</p>'

    helper_test_functions.clear(url)

def test_profile_setemail_token_incorrect(url):
    '''
    This test uses the feature user/profile/setemail with an invalid token. The
    expected outcome is an error of 400 saying 'Token is incorrect'
    '''
    response = helper_test_functions.user_profile_setemail('0', "j@hotmail.com", url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Token is incorrect</p>'

    helper_test_functions.clear(url)

def test_profile_setemail_correct_update(url):
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
        url
    )
    new_user = response
    u_id = new_user['u_id']
    token = new_user['token']

    # input valid handle_str into user/profile
    error = helper_test_functions.user_profile_setemail(token, "jay@gmail.com", url)

    assert error == {}
    users = helper_test_functions.users_all(token, url)

    for user in users['users']:
        if user['u_id'] == u_id:
            assert user['email'] == "jay@gmail.com"

    # clears data
    helper_test_functions.clear(url)
