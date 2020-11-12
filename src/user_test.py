'''
Tests for user.py
16/10/20
'''
import pytest
import channel
import channels
import auth
import user
from data import data
from error import InputError, AccessError
from other import clear


#################### Tests for user/profile/uploadphoto ########################

def test_profile_upload_invalid_token():
    '''
    This test uses the feature user/profile/uploadphoto with an invalid token.
    The expected outcome is giving an error of 400 saying 'Token is incorrect'.
    '''

    with pytest.raises(AccessError) as e:
        user.user_profile_photo("token", "https://cdn.hipwallpaper.com/i/83/61/uTbGH2.jpg", 0, 0, 1000, 1000)
    assert str(e.value) == '400 Bad Request: Token is incorrect'

    clear()

# The rest of the profile photo tests are in user_test_http.py

#################### Tests for user/profile/uploadphoto ########################

def test_profile_upload_invalid_token(url):
    '''
    This test uses the feature user/profile/uploadphoto with an invalid token.
    The expected outcome is giving an error of 400 saying 'Token is incorrect'.
    '''

    # input invalid token into user/profile/uploadphoto
    response = helper_test_functions.user_profile_uploadphoto(
        "token",
        "https://cdn.hipwallpaper.com/i/83/61/uTbGH2.jpg",
        0,
        0,
        1000,
        1000,
        url
    )
    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Token is incorrect</p>'

    # clears data
    helper_test_functions.clear(url)


def test_profile_upload_invalid_img_url(url):
    '''
    This test uses the feature user/profile/uploadphoto with an invalid img_url.
    The expected outcome is giving an error of 400 saying 'Provided url is not a
    valid jpg image url'.
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
    token = new_user["token"]

    # input invalid img_url into user/profile/uploadphoto
    response = helper_test_functions.user_profile_uploadphoto(
        token,
        "https://steamuserimages-a.akamaihd.net/ugc/794258384795697139/C32444A60986B8EE67E9CAEFD434F9EBB48BDB",
        0,
        0,
        1000,
        1000,
        url
    )
    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>img_url returned an HTTP status other than 200</p>'

    # clears data
    helper_test_functions.clear(url)

def test_profile_upload_png_img_url(url):
    '''
    This test uses the feature user/profile/uploadphoto with an valid png img_url.
    The expected outcome is giving an error of 400 saying 'Provided url is not a
    valid jpg image url'.
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
    token = new_user["token"]

    # input an png_img_url into user/profile/uploadphoto
    response = helper_test_functions.user_profile_uploadphoto(
        token,
        "https://static.wikia.nocookie.net/projectsekai/images/6/6a/Miku.png/revision/latest?cb=20200213214056",
        0,
        0,
        1000,
        1000,
        url
    )
    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Provided url is not a valid jpg image url</p>'

    # clears data
    helper_test_functions.clear(url)

def test_profile_upload_invalid_crop_size(url):
    '''
    This test uses the feature user/profile/uploadphoto with an invalid crop size.
    The expected outcome is giving an error of 400 saying 'Invalid crop size, the
    image has dimensions 'x' x 'y''.
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
    token = new_user["token"]

    # input invalid crop_size into user/profile/uploadphoto
    response = helper_test_functions.user_profile_uploadphoto(
        token,
        "https://i.pinimg.com/736x/3f/b3/f7/3fb3f7a82af56d4cb917e95a69af8d28.jpg",
        0,
        0,
        1000,
        1000,
        url
    )
    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Invalid crop size, the image has dimensions 600 x 338</p>'

    # clears data
    helper_test_functions.clear(url)

def test_profile_upload_correct_crop_size(url):
    '''
    This test uses the feature user/profile/uploadphoto with an valid crop size.
    The expected outcome is an image url with the correct crop size in the user's
    profile_img_url.
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
    token = new_user["token"]

    # input valid info into user/profile/uploadphoto
    helper_test_functions.user_profile_uploadphoto(
        token,
        "https://i.pinimg.com/736x/3f/b3/f7/3fb3f7a82af56d4cb917e95a69af8d28.jpg",
        5,
        20,
        200,
        220,
        url
    )

    image_object = Image.open("src/static/user_profile_pic_1.jpg")
    image_size = image_object.size
    assert image_size[0] == 195
    assert image_size[1] == 200

    response = helper_test_functions.user_profile(token, 1, url)
    profile = response
    profile_img_url = profile['profile_img_url']
    # omit the url as it will be different everytime
    assert profile_img_url.split('/',3)[3] == 'static/user_profile_pic_1.jpg'

    # clears data
    helper_test_functions.clear(url)

########################### Tests for user/profile #############################

def test_profile_invalid_user_token():
    '''
    This test uses the feature user/profile with an invalid token. The expected
    outcome is giving an error of 400 saying 'Token is incorrect'.
    '''
    # register first user
    auth.auth_register('jack@gmail.com', 'jkrsfunland', 'Jack', 'Napier')

    # input invalid token into user/profile
    with pytest.raises(AccessError) as e:
        user.user_profile("token", 1)
    assert str(e.value) == '400 Bad Request: Token is incorrect'

    # clears data
    clear()

def test_profile_u_id_not_found():
    '''
    This test uses the feature user/profile with an invalid u_id. The expected
    outcome is giving an error of 400 saying 'No users with the entered u_id was
    found'.
    '''
    # register first user
    jack = auth.auth_register('jack@gmail.com', 'jkrsfunland', 'Jack', 'Napier')

    # input invalid token into user/profile
    with pytest.raises(InputError) as e:
        user.user_profile(jack['token'], 2)
    assert str(e.value) == '400 Bad Request: No users with the entered u_id was found'

    # clears data
    clear()

def test_profile_display_correct_info():
    '''
    This test uses the feature user/profile with an valid inputs. The expected
    outcome is an dictonary of u_id, email, first name, last name and handle of
    the user with the inputted u_id.
    '''
    # register first user
    marko = auth.auth_register('markowong@hotmail.com', 'jkrsfunland', 'marko', 'wong')

    # display profile of the caller
    response = user.user_profile(marko['token'], 1)

    profile = response['user']
    assert profile['u_id'] == marko['u_id']
    assert profile['email'] == "markowong@hotmail.com"
    assert profile['name_first'] == "marko"
    assert profile['name_last'] == "wong"
    assert profile['handle_str'] == "markowong"

    # register second user
    marko2 = auth.auth_register('markowong2@hotmail.com', 'jkrsfunland', 'marko2', 'wong2')

    # display profile of another user called from the first user
    response = user.user_profile(marko['token'], 2)
    profile = response['user']
    assert profile['u_id'] == marko2['u_id']
    assert profile['email'] == "markowong2@hotmail.com"
    assert profile['name_first'] == "marko2"
    assert profile['name_last'] == "wong2"
    assert profile['handle_str'] == "marko2wong2"

    # clears data
    clear()

###################### Tests for user/profile/sethandle ########################

def test_profile_handle_invalid_user_token():
    '''
    This test uses the feature user/profile/sethandle with an invalid token. The
    expected outcome is an error of 400 saying 'Token is incorrect'
    '''
    # input invalid token into user/profile/sethandle
    with pytest.raises(AccessError) as e:
        user.user_profile_sethandle("token", 1)
    assert str(e.value) == '400 Bad Request: Token is incorrect'

    # clears data
    clear()

def test_profile_handle_too_short():
    '''
    This test uses the feature user/profile/sethandle with an invalid handle that
    is too short. Theexpected outcome is an error of 400 saying 'Handle length
    needs to be between 3 and 20.
    '''
    # register first user
    marko = auth.auth_register('marko@hotmail.com', 'jkrsfund', 'marko', 'wong')

    # input invalid handle into user/profile/sethandle
    with pytest.raises(InputError) as e:
        user.user_profile_sethandle(marko['token'], "Mr")
    assert str(e.value) == '400 Bad Request: Handle length needs to be between 3 and 20'

    # clears data
    clear()
    
def test_profile_handle_too_long():
    '''
    This test uses the feature user/profile/sethandle with an invalid handle that
    is too long. The expected outcome is an error of 400 saying 'Handle length
    needs to be between 3 and 20.
    '''
    # register first user
    marko = auth.auth_register('marko@hotmail.com', 'jkrsfund', 'marko', 'wong')

    # input invalid handle into user/profile/sethandle
    with pytest.raises(InputError) as e:
        user.user_profile_sethandle(marko['token'], "MrCooloMrcoolface123456789")
    assert str(e.value) == '400 Bad Request: Handle length needs to be between 3 and 20'

    # clears data
    clear()

def test_profile_handle_exisiting():
    '''
    This test uses the feature user/profile/sethandle with an duplicate handle.
    The expected outcome is an error of 400 saying 'Handle already in use by
    another user.
    '''
    # register first user
    marko = auth.auth_register('marko@hotmail.com', 'jkrsfund', 'marko', 'wong')

    # input valid handle_str into user/profile
    user.user_profile_sethandle(marko['token'], "Yes plz 10/10")

    # register second user
    auth.auth_register('marko2@hotmail.com', 'jkrsfund', 'marko2', 'wong2')

    # input a valid duplicate handle_str into user/profile/sethandle
    with pytest.raises(InputError) as e:
        user.user_profile_sethandle(marko['token'], "Yes plz 10/10")
    assert str(e.value) == '400 Bad Request: Handle already in use by another user'

    # clears data
    clear()

def test_profile_handle_correct_update():
    '''
    This test uses the feature user/profile/sethandle with valid inputs. The
    expected outcome is that the handle string stored in the database will change
    to the input handle string.
    '''
    # register first user
    marko = auth.auth_register('marko@hotmail.com', 'jkrsfund', 'marko', 'wong')

    # input valid handle_str into user/profile/sethandle
    user.user_profile_sethandle(marko['token'], "Yes plz 10/10")

    #users = other.users_all(marko['token'])
    # Grabs all users from data
    users = data['users']
    for curr_user in users:
        if curr_user['u_id'] == marko['u_id']:
            assert curr_user['handle_str'] == "Yes plz 10/10"

    # clears data
    clear()

###################### Tests for user/profile/setname ##########################

def test_profile_setname_correct_update():
    '''
    This test uses the feature user/profile/setname with valid inputs. The
    expected outcome is the name_first string and name_last string stored in the
    database will change to the inputted strings.
    '''
    # register first user
    marko = auth.auth_register('marko@hotmail.com', 'jkrsfund', 'marko', 'wong')

    # input valid handle_str into user/profile/setname
    user.user_profile_setname(marko['token'], "Nikhil", "wongsta")

    #users = other.users_all(marko['token'])
    # Grabs all users from data
    users = data['users']
    for curr_user in users:
        if curr_user['u_id'] == marko['u_id']:
            assert curr_user['name_first'] == "Nikhil"
            assert curr_user['name_last'] == "wongsta"

    # clears data
    clear()

def test_profile_setname_last_name_too_short():
    '''
    This test uses the feature user/profile/setname with an invalid name_last
    that is too short. The expected outcome is an error of 400 saying 'Handle
    length needs to be between 3 and 20.
    '''
    # register first user
    marko = auth.auth_register('marko@hotmail.com', 'jkrsfund', 'marko', 'wong')

    # input invalid handle into user/profile/setname
    with pytest.raises(InputError) as e:
        user.user_profile_setname(marko['token'], "soko", "")
    assert str(e.value) == '400 Bad Request: Last name must be between 1 and 50 characters in length'

    # clears data
    clear()

def test_profile_setname_last_name_too_long():
    '''
    This test uses the feature user/profile/setname with an invalid name_last
    that is too long. The expected outcome is an error of 400 saying 'Handle
    length needs to be between 3 and 20.
    '''
     # register first user
    marko = auth.auth_register('marko@hotmail.com', 'jkrsfund', 'marko', 'wong')

    # input invalid handle into user/profile/setname
    with pytest.raises(InputError) as e:
        user.user_profile_setname(marko['token'], "soko", "pkadsngkpnqkfnkpasmkfmpkqjef padjdfpj apsdfasfaesfasf qw")
    assert str(e.value) == '400 Bad Request: Last name must be between 1 and 50 characters in length'

    # clears data
    clear()

def test_profile_setname_first_name_too_short():
    '''
    This test uses the feature user/profile/setname with an invalid name_first
    that is too short. The expected outcome is an error of 400 saying 'Handle
    length needs to be between 3 and 20.
    '''
    # register first user
    marko = auth.auth_register('marko@hotmail.com', 'jkrsfund', 'marko', 'wong')

    # input invalid handle into user/profile/setname
    with pytest.raises(InputError) as e:
        user.user_profile_setname(marko['token'], "", "yoko")
    assert str(e.value) == '400 Bad Request: First name must be between 1 and 50 characters in length'

    # clears data
    clear()

def test_profile_setname_first_name_too_long():
    '''
    This test uses the feature user/profile/setname with an invalid name_first
    that is too long. The expected outcome is an error of 400 saying 'Handle
    length needs to be between 3 and 20.
    '''
    # register first user
    marko = auth.auth_register('marko@hotmail.com', 'jkrsfund', 'marko', 'wong')

    # input invalid handle into user/profile/setname
    with pytest.raises(InputError) as e:
        user.user_profile_setname(marko['token'], "", "pkwqfp[osaf apos[of qqfaposfmqealfknqeafszk;xfm")
    assert str(e.value) == '400 Bad Request: First name must be between 1 and 50 characters in length'

    # clears data
    clear()


def test_profile_setname_token_incorrect():
    '''
    This test uses the feature user/profile/setname with an invalid token. The
    expected outcome is an error of 400 saying 'Token is incorrect'
    '''
    # input invalid token into user/profile
    with pytest.raises(AccessError) as e:
        user.user_profile_setname("token", "soko", "yoko")
    assert str(e.value) == '400 Bad Request: Token is incorrect'

    # clears data
    clear()

###################### Tests for user/profile/setemail #########################

def test_profile_setemail_not_valid():
    '''
    This test uses the feature user/profile/setemail with an invalid email. The
    expected outcome is an error of 400 saying 'Email is not valid'
    '''
    # register first user
    marko = auth.auth_register('marko@hotmail.com', 'jkrsfund', 'marko', 'wong')

    # input invalid handle into user/profile/setemail
    with pytest.raises(InputError) as e:
        user.user_profile_setemail(marko['token'], "jacknapier.com")
    assert str(e.value) == '400 Bad Request: Email is not valid'

    # clears data
    clear()

def test_set_email_used():
    '''
    This test uses the feature user/profile/setemail with an duplicate email.
    The expected outcome is an error of 400 saying 'Email address is already in
    use.
    '''
    # register first user
    marko = auth.auth_register('marko@hotmail.com', 'jkrsfund', 'marko', 'wong')

    # input valid handle_str into user/profile/setemail
    user.user_profile_setemail(marko['token'], "marko3@hotmail.com")

    # register second user
    marko2 = auth.auth_register('marko2@hotmail.com', 'jkrsfund', 'marko2', 'wong2')

    # input a valid duplicate handle_str into user/profile/setemail
    with pytest.raises(InputError) as e:
        user.user_profile_setemail(marko2['token'], "marko3@hotmail.com")
    assert str(e.value) == '400 Bad Request: Email address is already in use'

    # clears data
    clear()

def test_profile_setemail_token_incorrect():
    '''
    This test uses the feature user/profile/setemail with an invalid token. The
    expected outcome is an error of 400 saying 'Token is incorrect'
    '''
     # input invalid token into user/profile/setemail
    with pytest.raises(AccessError) as e:
        user.user_profile_setemail("token", "validemail@email.com")
    assert str(e.value) == '400 Bad Request: Token is incorrect'

    # clears data
    clear()

def test_profile_setemail_correct_update():
    '''
    This test uses the feature user/profile/setemail with valid inputs. The
    expected outcome is the email assoicate the user who calls this function will
    have their email changed in the database.
    '''
    # register first user
    marko = auth.auth_register('marko@hotmail.com', 'jkrsfund', 'marko', 'wong')

    # input valid handle_str into user/profile/sethandle
    user.user_profile_setemail(marko['token'], "yesplz@10outof10.com")

    #users = other.users_all(marko['token'])
    # Grabs all users from data
    users = data['users']
    for curr_user in users:
        if curr_user['u_id'] == marko['u_id']:
            assert curr_user['email'] == "yesplz@10outof10.com"

    # clears data
    clear()
