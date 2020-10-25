# Written on 24/09/2020
# Purpose to test functions in channel.py
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import pytest
from data import data
import helper_test_functions

import channel
import channels
import auth
from error import InputError, AccessError
from other import clear
from fixture import url as _url

#@pytest.fixture
#def _url():
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

######################### Tests for channel/invite #############################
def test_channel_invite_token_incorrect(_url):
    '''
    This test uses the feature channel/invite with an invalid token. The
    expected outcome is an error of 400 saying 'Token is incorrect'
    '''
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user_1 = response
    u_id_1 = new_user_1['u_id']
    token_1 = new_user_1['token']

    response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
    new_channel = response
    channel_id = new_channel['channel_id']

    assert channel_id == 1
    response = helper_test_functions.channel_invite("0", channel_id, u_id_1, _url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Token is incorrect</p>'

    requests.delete(_url + '/clear')
    
def test_channel_invite_invalid_channel_id(_url):
    '''
    This test uses the feature channel/invite with an invalid channel_id. The
    expected outcome is error of 400 saying 'Channel_id does not exist'.
    '''
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user_1 = response
    token_1 = new_user_1['token']

    response = helper_test_functions.auth_register(
        "markowong2@hotmail.com",
        "markowong2",
        "marko2",
        "wong2",
        _url
    )
    new_user_2 = response
    u_id_2 = new_user_2['u_id']

    response = helper_test_functions.channel_invite(token_1, 0, u_id_2, _url)
    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Channel_id does not exist</p>'
    requests.delete(_url + '/clear')

def test_channel_invite_invalid_user_id(_url):
    '''
    This test uses the feature channel/invite with an invalid user_id. The
    expected outcome is error of 400 saying 'user_id does not exist'.
    '''
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user_1 = response
    token_1 = new_user_1['token']

    response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
    new_channel = response
    channel_id = new_channel['channel_id']

    response = helper_test_functions.channel_invite(token_1, channel_id, 2, _url)
    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>user_id does not exist</p>'
    requests.delete(_url + '/clear')

def test_channel_invite_user_not_in_channel(_url):
    '''
    This test uses the feature channel/invite with an user_id that is already in
    the channel. The expected outcome is error of 400 saying 'Authorised user is
    not a member of the channel'.
    '''
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user_1 = response
    token_1 = new_user_1['token']

    response = helper_test_functions.auth_register(
        "markowong2@hotmail.com",
        "markowong2",
        "marko2",
        "wong2",
        _url
    )
    new_user_2 = response
    token_2 = new_user_2['token']

    response = helper_test_functions.auth_register(
        "markowong3@hotmail.com",
        "markowong3",
        "marko3",
        "wong3",
        _url
    )
    new_user_3 = response
    u_id_3 = new_user_3['u_id']

    response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
    new_channel = response
    channel_id = new_channel['channel_id']

    response = helper_test_functions.channel_invite(token_2, channel_id, u_id_3, _url)
    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Authorised user is not a member of the channel</p>'
    requests.delete(_url + '/clear')


def test_channel_invite_working(_url): 
    '''
    This test uses the feature channel/invite with valid inputs. The expected
    utcome is the invited user is added to the channel immediately.
    '''
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user_1 = response
    token_1 = new_user_1['token']

    response = helper_test_functions.auth_register(
        "markowong2@hotmail.com",
        "markowong2",
        "marko2",
        "wong2",
        _url
    )
    new_user_2 = response
    token_2 = new_user_2['token']
    u_id_2 = new_user_2['u_id']

    response = helper_test_functions.auth_register(
        "markowong3@hotmail.com",
        "markowong3",
        "marko3",
        "wong3",
        _url
    )
    new_user_3 = response
    u_id_3 = new_user_3['u_id']

    response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
    new_channel = response
    channel_id = new_channel['channel_id']

    # invite users to channel
    helper_test_functions.channel_invite(token_1, channel_id, u_id_2, _url)
    helper_test_functions.channel_invite(token_2, channel_id, u_id_3, _url)
    
    # check that the users are in the channel
    response = helper_test_functions.channels_list(token_1, _url)
    memebers = response['channels'][0]['members']
    assert memebers[0]['name_first'] == 'marko'
    assert memebers[1]['name_first'] == 'marko2'
    assert memebers[2]['name_first'] == 'marko3'

######################### Tests for channel/details ############################
def test_channel_details_invalid_token(_url):
    '''
    This test uses the feature channel/details with an invalid token. The
    expected outcome is an error of 400 saying 'Token is incorrect'
    '''
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user_1 = response
    token_1 = new_user_1['token']

    response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
    new_channel = response
    channel_id = new_channel['channel_id']

    response = helper_test_functions.channel_details("0", channel_id, _url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Token is incorrect</p>'

    requests.delete(_url + '/clear')

def test_channel_details_invalid_channel_id(_url):
    '''
    This test uses the feature channel/details with an invalid channel_id. The
    expected outcome is an error of 400 saying 'Channel_id does not exist'
    '''
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user_1 = response
    token_1 = new_user_1['token']

    response = helper_test_functions.channel_details(token_1, 1, _url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Channel_id does not exist</p>'

    requests.delete(_url + '/clear')

def test_channel_details_user_not_a_member(_url):
    '''
    This test uses the feature channel/detials with an user_id that is not in
    the channel. The expected outcome is error of 400 saying 'Authorised user is
    not a member of the channel'.
    '''
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user_1 = response
    token_1 = new_user_1['token']

    response = helper_test_functions.auth_register(
        "markowong2@hotmail.com",
        "markowong2",
        "marko2",
        "wong2",
        _url
    )
    new_user_2 = response
    token_2 = new_user_2['token']

    response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
    new_channel = response
    channel_id = new_channel['channel_id']

    response = helper_test_functions.channel_details(token_2, channel_id, _url)
    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Authorised user is not a member of the channel</p>'
    requests.delete(_url + '/clear')

def test_channel_detail_working(_url):
    '''
    This test uses the feature channel/detials with valid inputs. The expected
    outcome is providing basic details about the channel including: name,
    owner_members, all_members.
    '''
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user_1 = response
    token_1 = new_user_1['token']

    response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
    new_channel = response
    channel_id = new_channel['channel_id']

    response = helper_test_functions.channel_details(token_1, channel_id, _url)
    assert response['owner_members'][0]['name_first'] == 'marko'
    assert response['all_members'][0]['name_first'] == 'marko'

######################### Tests for channel/messages ###########################
def test_channel_messages_invalid_token(_url):
    '''
    This test uses the feature channel/messages with an invalid token. The
    expected outcome is an error of 400 saying 'Token is incorrect'
    '''
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user_1 = response
    token_1 = new_user_1['token']

    response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
    new_channel = response
    channel_id = new_channel['channel_id']

    response = helper_test_functions.channel_messages("0", channel_id, 0, _url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Token is incorrect</p>'

    requests.delete(_url + '/clear')

def test_channel_messages_invalid_channel_id(_url):
    '''
    This test uses the feature channel/messages with an invalid channel_id. The
    expected outcome is an error of 400 saying 'Channel_id does not exist'
    '''

    user_1 = helper_test_functions.auth_register(
        "123@hotmail.com", 
        "password", 
        "Bobby", 
        "McBob",
        _url
    )
   
    new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True, _url)

    error = helper_test_functions.channel_messages(user_1['token'], new_channel['channel_id'], 0, _url)



    assert error['code'] == 400
    assert error['message'] == '<p>Channel_id does not exist</p>'
    
    requests.delete(_url + '/clear')

def test_channel_messages_start_greater(_url): #NOT DONE
    '''
    This test uses the feature channel/messages with an invalid start. The
    expected outcome is an error of 400 saying 'Start is greater than total
    number of messages'.
    '''
'''
    user_1 = helper_test_functions.auth_register(
        "123@hotmail.com", 
        "password", 
        "Bobby", 
        "McBob",
        _url
    )
   
    new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True, _url)
    channel_id = new_channel['channel_id']

    error = helper_test_functions.channel_messages(user_1['token'], new_channel['channel_id'], 100, _url)
    
    assert error['code'] == 400
    assert error['message'] == '<p>Start is greater than total number of messages</p>'
    requests.delete(_url + '/clear')
    
    # getting {'code': 400, 'name': 'System Error', 'message': '<p>Channel_id does not exist</p>'}    
'''    
def test_channel_messages_user_not_a_member(_url): #NOT DONE
    '''
    This test uses the feature channel/messages with an user_id that is not in
    the channel. The expected outcome is error of 400 saying 'Authorised user is
    not a member of the channel'.
    '''
'''
    user_1 = helper_test_functions.auth_register(
        "markowong2@hotmail.com",
        "markowong2",
        "marko2",
        "wong2",
        _url
    )

    
    user_2 = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )

    new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True, _url)


   
    response = helper_test_functions.channel_messages(user_2['token'], new_channel['channel_id'],0, _url)
    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Authorised user is not a member of the channel</p>'
    requests.delete(_url + '/clear')
     # getting {'code': 400, 'name': 'System Error', 'message': '<p>Channel_id does not exist</p>'} 
'''
def test_channel_messages_working(_url): #NOT DONE
    '''
    This test uses the feature channel/messages with valid inputs. The expected
    outcome is dictories of messages, start, end 
    '''
'''
     user_1 = helper_test_functions.auth_register(
        "markowong2@hotmail.com",
        "markowong2",
        "marko2",
        "wong2",
        _url
    )

    
    
    new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True, _url)
   
    response = helper_test_functions.channel_messages(user_1['token'], new_channel['channel_id'],0, _url)
    
'''    

########################## Tests for channel/leave #############################
def test_channel_leave_invalid_token(_url):
    '''
    This test uses the feature channel/leave with an invalid token. The
    expected outcome is an error of 400 saying 'Token is incorrect'
    '''
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user_1 = response
    token_1 = new_user_1['token']

    response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
    new_channel = response
    channel_id = new_channel['channel_id']

    response = helper_test_functions.channel_leave("0", channel_id, _url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Token is incorrect</p>'

    requests.delete(_url + '/clear')

def test_channel_leave_invalid_channel_id(_url):
    '''
    This test uses the feature channel/leave with an invalid channel_id. The
    expected outcome is an error of 400 saying 'Channel_id does not exist'
    '''

    user_1 = helper_test_functions.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob",
        _url
    )

    error = helper_test_functions.channel_leave(user_1['token'], 1, _url)
    assert error['code'] == 400
    assert error['message'] == '<p>Channel_id does not exist</p>'

    helper_test_functions.clear(_url)

def test_channel_leave_user_not_a_member(_url):
    '''
    This test uses the feature channel/leave with an user_id that is not in
    the channel. The expected outcome is error of 400 saying 'Authorised user is
    not a member of the channel'.
    '''
    user_1 = helper_test_functions.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob",
        _url
    )
    new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True, _url)

    user_2 = helper_test_functions.auth_register(
        "bestanime@hotmail.com",
        "Goku is mid!",
        "mei",
        "wei",
        _url
    )
    channel_id = new_channel['channel_id']

    error = helper_test_functions.channel_leave(user_2['token'], channel_id, _url)
    assert error['code'] == 400
    assert error['message'] == '<p>Authorised user is not a member of the channel</p>'

    helper_test_functions.clear(_url)

def test_channel_leave_working(_url):
    '''
    This test uses the feature channel/leave with valid inputs. The expected
    outcome is that the database removes that user from the list of members for
    that channel.
    '''

    response = helper_test_functions.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob",
        _url
    )
    new_user_1 = response
    token_1 = new_user_1['token']
    new_channel = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
    channel_id = new_channel['channel_id']

    response = helper_test_functions.auth_register(
        "markowong2@hotmail.com",
        "markowong2",
        "marko2",
        "wong2",
        _url
    )
    new_user_2 = response
    token_2 = new_user_2['token']
    u_id_2 = new_user_2['u_id']


    helper_test_functions.channel_invite(token_1, channel_id, u_id_2, _url)
    helper_test_functions.channel_leave(token_2, channel_id, _url)

    response = helper_test_functions.channel_details(token_1, channel_id, _url)
    assert len(response['all_members']) == 1

    helper_test_functions.clear(_url)

########################### Tests for channel/join #############################
def test_channel_join_invalid_token(_url):
    '''
    This test uses the feature channel/join with an invalid token. The
    expected outcome is an error of 400 saying 'Token is incorrect'
    '''
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user_1 = response
    token_1 = new_user_1['token']

    response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
    new_channel = response
    channel_id = new_channel['channel_id']

    response = helper_test_functions.channel_join("0", channel_id, _url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Token is incorrect</p>'

    requests.delete(_url + '/clear')

def test_channel_join_invalid_channel_id(_url): 
    '''
    This test uses the feature channel/join with an invalid channel_id. The
    expected outcome is an error of 400 saying 'Channel_id does not exist'
    '''
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user_1 = response
    token_1 = new_user_1['token']

    response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)

    response = helper_test_functions.channel_join(token_1, 909, _url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Channel_id does not exist</p>'

    requests.delete(_url + '/clear')

def test_channel_join_user_not_a_member(_url):
    '''
    This test uses the feature channel/join with an user_id that is not in
    the channel. The expected outcome is error of 400 saying 'Channel_id refers
    to a channel that is private
    '''

    user_1 = helper_test_functions.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob",
        _url
    )
    new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', False, _url)

    user_2 = helper_test_functions.auth_register(
        "bestanime@hotmail.com",
        "Goku is mid!",
        "mei",
        "wei",
        _url
    )
    channel_id = new_channel['channel_id']

    error = helper_test_functions.channel_join(user_2['token'], channel_id, _url)
    assert error['code'] == 400
    assert error['message'] == '<p>Channel_id refers to a channel that is private</p>'

    helper_test_functions.clear(_url)

def test_channel_join_working(_url): 
    '''
    This test uses the feature channel/join with valid inputs. The expected
    outcome is that the database adds that user to the list of members for that
    public channel.
    '''
    response = helper_test_functions.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob",
        _url
    )
    new_user_1 = response
    token_1 = new_user_1['token']
    new_channel = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
    channel_id = new_channel['channel_id']

    response = helper_test_functions.auth_register(
        "markowong2@hotmail.com",
        "markowong2",
        "marko2",
        "wong2",
        _url
    )
    new_user_2 = response
    token_2 = new_user_2['token']

    helper_test_functions.channel_join(token_2, channel_id, _url)

    response = helper_test_functions.channel_details(token_1, channel_id, _url)
    assert len(response['all_members']) == 2

    helper_test_functions.clear(_url)

######################## Tests for channel/addowner ############################
def test_channel_addowner_invalid_token(_url):
    '''
    This test uses the feature channel/addowner with an invalid token. The
    expected outcome is an error of 400 saying 'Token is incorrect'
    '''
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user_1 = response
    u_id_1 = new_user_1['token']
    token_1 = new_user_1['token']

    response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
    new_channel = response
    channel_id = new_channel['channel_id']

    response = helper_test_functions.channel_addowner("0", channel_id, u_id_1, _url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Token is incorrect</p>'

    requests.delete(_url + '/clear')

def test_channel_addowner_invalid_channel_id(_url): 
    '''
    This test uses the feature channel/addowner with an invalid channel_id. The
    expected outcome is an error of 400 saying 'Channel_id does not exist'
    '''
    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user_1 = response
    u_id_1 = new_user_1['token']
    token_1 = new_user_1['token']

    response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)

    response = helper_test_functions.channel_addowner(token_1, 909, u_id_1, _url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Channel_id does not exist</p>'

    requests.delete(_url + '/clear')
def test_channel_addowner_user_not_a_member(_url): 
    '''
    This test uses the feature channel/addowner with an user_id that is not in
    the channel. The expected outcome is error of 400 saying 'Authorised user is
    not an owner of the channel'.
    '''
  
    user_1 = helper_test_functions.auth_register(
        "123@hotmail.com", 
        "password", 
        "Bobby", 
        "McBob",
        _url
    )
    new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True, _url)
    
    user_2 = helper_test_functions.auth_register(
        "bestanime@hotmail.com",
        "Goku is mid!", 
        "mei", 
        "wei", 
        _url
    )
    channel_id = new_channel['channel_id']

    error = helper_test_functions.channel_addowner(user_2['token'], channel_id, user_2['u_id'],  _url)
    assert error['code'] == 400
    assert error['message'] == '<p>Authorised user is not an owner of the channel</p>'
    
    requests.delete(_url + '/clear')

def test_channel_addowner_working(_url): #NOT DONE
    '''
    This test uses the feature channel/addowner with valid inputs. The expected
    outcome is that the database adds that user to the list of owner_members for
    that channel.
    '''
####################### Tests for channel/removeowner ##########################

def test_channel_removeowner_invalid_token(_url): 
    '''
    This test uses the feature channel/removeowner with an invalid token. The
    expected outcome is an error of 400 saying 'Token is incorrect'
    '''

    response = helper_test_functions.auth_register(
        "markowong@hotmail.com",
        "markowong",
        "marko",
        "wong",
        _url
    )
    new_user_1 = response
    u_id_1 = new_user_1['token']
    token_1 = new_user_1['token']

    response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
    new_channel = response
    channel_id = new_channel['channel_id']

    response = helper_test_functions.channel_removeowner("0", channel_id, u_id_1, _url)

    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Token is incorrect</p>'

    requests.delete(_url + '/clear')

def test_channel_removeowner_invalid_channel_id(_url): 
    '''
    This test uses the feature channel/removeowner with an invalid channel_id. The
    expected outcome is an error of 400 saying 'Channel_id does not exist'
    '''
   
    user_1 = helper_test_functions.auth_register(
        "123@hotmail.com", 
        "password", 
        "Bobby", 
        "McBob",
        _url
    )
    
    user_2 = helper_test_functions.auth_register(
        "bestanime@hotmail.com",
        "Goku is mid!", 
        "mei", 
        "wei", 
        _url
    )
    channel_1 = helper_test_functions.channels_create(user_1['token'], "channel_1", True, _url)
    helper_test_functions.channel_addowner(user_1['token'], channel_1['channel_id'], user_2['u_id'],_url)
    
    response = helper_test_functions.channel_removeowner(user_1['token'], 909, user_2['u_id'],_url)

    assert response["code"] == 400
    assert response["message"] == '<p>Channel_id does not exist</p>'
    requests.delete(_url + '/clear')
    
def test_channel_removeowner_user_not_a_member(_url):  
    '''
    This test uses the feature channel/removeowner with an user_id that is not in
    the channel. The expected outcome is error of 400 saying 'Authorised user is
    not an owner of the channel'.
    '''
    
    user_1 = helper_test_functions.auth_register(
        "123@hotmail.com", 
        "password", 
        "Bobby", 
        "McBob",
        _url
    )
    new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True, _url)
    
    user_2 = helper_test_functions.auth_register(
        "bestanime@hotmail.com",
        "Goku is mid!", 
        "mei", 
        "wei", 
        _url
    )
    channel_id = new_channel['channel_id']

    error = helper_test_functions.channel_removeowner(user_2['token'], channel_id, user_2['u_id'], _url)
    assert error['code'] == 400
    assert error['message'] == '<p>Authorised user is not an owner of the channel</p>'
    
    helper_test_functions.clear(_url)

def test_channel_removeowner_working(_url): #NOT DONE
    '''
    This test uses the feature channel/removeowner with valid inputs. The expected
    outcome is that the database removes that user from the list of owners_members
    for that channel.
    '''







'''
def test_channel():
    bruce = helper_test_functions.auth_register('bruce@gmail.com', 'batm4n23', 'Bruce', 'Wayne',_url)
    wayne = helper_test_functions.auth_register('wayne@gmail.com', 'zorro#', 'Wayne', 'Thomas',_url)
    alfred = helper_test_functions.auth_register('alfred@gmail.com', 'wayneman0r', 'Alfred', 'Pennyworth',_url)
    jack = helper_test_functions.auth_register('jack@gmail.com', 'jkrsfunland', 'Jack', 'Napier',_url)
    
    batcave_channel = helper_test_functions.channels_create(bruce['token'], 'batcave_channel', True,_url)
    manor_channel = helper_test_functions.channels_create(wayne['token'], 'batcave_channel', False,_url)

    ch_details = helper_test_functions.channel_details(bruce['token'], batcave_channel['channel_id'],_url)
    assert len(ch_details['owner_members']) == len(ch_details['all_members']) == 1

    # Test if members are added correctly when joining
    helper_test_functions.channel_join(alfred['token'], batcave_channel['channel_id'],_url)
    assert len(ch_details['all_members']) == 2
    
    no_id_response = helper_test_functions.channel_join(alfred['token'], 909,_url)
    assert no_id_response["code"] == 400
    assert no_id_response["message"] == '<p>Channel_id does not exist<p>'
    
    private_response = helper_test_functions.channel_join(alfred['token'], manor_channel['channel_id'], _url)
    assert private_response["code"] == 400
    assert private_response["message"] == '<p>Channel_id refers to a channel that is private<p>'

    no_id_response = helper_test_functions.channel_addowner(wayne['token'], 909, alfred['u_id'], _url)
    assert no_id_response["code"] == 400
    assert no_id_response["message"] == '<p>Channel_id does not exist<p>'
    
    owner_response = helper_test_functions.channel_addowner(wayne['token'], batcave_channel['channel_id'], alfred['u_id'], _url)
    assert owner_response["code"] == 400
    assert owner_response["message"] == '<p>Authorised user is not an owner of the channel<p>'

    # Test if owners are added correctly
    helper_test_functions.channel_addowner(bruce['token'], batcave_channel['channel_id'], alfred['u_id'], _url)
    ch_details = helper_test_functions.channel_details(bruce['token'], batcave_channel['channel_id'], _url)
    assert len(ch_details['owner_members']) == 2

    response = helper_test_functions.channel_addowner(bruce['token'], batcave_channel['channel_id'], alfred['u_id'], _url)
    assert response["code"] == 400
    assert response["message"] == '<p>User is already an owner of the channel<p>'

  
    response = helper_test_functions.channel_addowner(bruce['token'], 909, alfred['u_id'], _url)
    assert response["code"] == 400
    assert response["message"] == '<p>Channel_id does not exist<p>'

    response = helper_test_functions.channel_addowner(wayne['token'], batcave_channel['channel_id'], alfred['u_id'], _url)
    assert response["code"] == 400
    assert response["message"] == '<p>Authorised user is not an owner of the channel<p>'

    helper_test_functions.channel_join(jack['token'], batcave_channel['channel_id'], _url)
    ch_details = helper_test_functions.channel_details(bruce['token'], batcave_channel['channel_id'], _url)
    assert len(ch_details['all_members']) == 3
    assert len(ch_details['owner_members']) == 2

    # Test channel_leave is implemented correctly 
    response = helper_test_functions.channel_leave(alfred['token'], 909, _url)
    assert response["code"] == 400
    assert response["message"] == '<p>Channel_id does not exist<p>'
    
    response = helper_test_functions.channel_leave(alfred['token'], manor_channel['channel_id'],_url)
    assert response["code"] == 400
    assert response["message"] == '<p>Authorised user is not a member of the channel<p>'


    helper_test_functions.channel_leave(alfred['token'], batcave_channel['channel_id'], _url)
    ch_details = channel.channel_details(bruce['token'], batcave_channel['channel_id'], _url)
    assert len(ch_details['all_members']) == 2
    assert len(ch_details['owner_members']) == 1

    # Test remove_owner
    helper_test_functions.channel_addowner(bruce['token'], batcave_channel['channel_id'], jack['u_id'],_url)
    ch_details = helper_test_functions.channel_details(bruce['token'], batcave_channel['channel_id'],_url)
    assert len(ch_details['owner_members']) == 2
    
    response = helper_test_functions.channel_removeowner(bruce['token'], batcave_channel['channel_id'], alfred['u_id'], _url)
    assert response["code"] == 400
    assert response["message"] == '<p>User with u_id is not an owner of the channel<p>'

    response = helper_test_functions.channel_removeowner(alfred['token'], batcave_channel['channel_id'], bruce['u_id'], _url)
    assert response["code"] == 400
    assert response["message"] == '<p>Authorised user is not an owner of the channel<p>'
    
    response = helper_test_functions.channel_removeowner(alfred['token'], 909, bruce['u_id'], _url)
    assert response["code"] == 400
    assert response["message"] == '<p>Channel_id does not exist<p>'    

    helper_test_functions.channel_removeowner(bruce['token'], batcave_channel['channel_id'], jack['u_id'],_url)
    ch_details = helper_test_functions.channel_details(bruce['token'], batcave_channel['channel_id'],_url)
    assert len(ch_details['owner_members']) == 1

    helper_test_functions.clear(_url)

# Test that public channel operates as expected
def test_channel_public():
    # Register users and have john set up a public channel
    john = helper_test_functions.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith',_url)
    bob = helper_test_functions.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime',_url)
    cool_channel = helper_test_functions.channels_create(john['token'], 'cool_channel', True,_url)


    ch_details = helper_test_functions.channel_details(john['token'], cool_channel['channel_id'],_url)
    assert ch_details['name'] == 'cool_channel'
    assert len(ch_details['owner_members']) == len(ch_details['all_members']) == 1

    # Check that new members are being added correctly
    helper_test_functions.channel_invite(john['token'], cool_channel['channel_id'], bob['u_id'],_url)
    ch_details = helper_test_functions.channel_details(john['token'], cool_channel['channel_id'],_url)

    assert ch_details['name'] == 'cool_channel'
    assert len(ch_details['owner_members']) == 1
    assert len(ch_details['all_members']) == 2
    
    # Check that members can leave
    helper_test_functions.channel_leave(bob['token'], cool_channel['channel_id'],_url)
    ch_details = channel.channel_details(john['token'], cool_channel['channel_id'],_url)
    assert len(ch_details['owner_members']) == 1 
    assert len(ch_details['all_members']) == 1
    
    # Check that members can join a public channel on their own
    helper_test_functions.channel_join(bob['token'], cool_channel['channel_id'],_url)
    ch_details = channel.channel_details(john['token'], cool_channel['channel_id'],_url)
    assert len(ch_details['owner_members']) == 1 
    assert len(ch_details['all_members']) == 2

    helper_test_functions.clear(_url)


# Test that private channel operates as expected
def test_channel_private():

    # Register three users and have John set up a private channel
    chicken = helper_test_functions.auth_register("hehe@hotmail.com", "qwerty", "Chicken", "Nugget", _url)
    john = helper_test_functions.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith', _url)
    bob = helper_test_functions.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime', _url)
    private_cool_channel = helper_test_functions.channels_create(john['token'], 'private_cool_channel', False,_url)

    # Joining a private channel should throw an error
    join_response = helper_test_functions.channel_join(chicken['token'], private_cool_channel['channel_id'], _url)
    assert join_response["code"] == 400
    assert join_response["message"] == "<p>Channel_id refers to a channel that is private</p>"

    # John adds an Chicken as an owner of the private channel
    addowner_response = helper_test_functions.channel_addowner(bob['token'], private_cool_channel['channel_id'], chicken['u_id'], _url)
    assert addowner_response["code"] == 400
    assert addowner_response["message"] == "<p>Authorised user is not an owner of the channel</p>"
    

    # Add chicken correctly
    helper_test_functions.channel_addowner(john['token'], private_cool_channel['channel_id'], chicken['u_id'], _url)
    # Inputting the incorrect channel id
    response = helper_test_functions.channel_addowner(chicken['token'], 'incorrect_channel', bob['u_id'], _url)
    assert response["code"] == 400
    assert response["message"] == "<p>Channel_id does not exist</p>"
    
    # Trying to invite a user that is already an owner 
    invite_response = helper_test_functions.channel_addowner(chicken['token'], private_cool_channel['channel_id'], john['u_id'], _url)
    assert invite_response["code"] == 400
    assert invite_response["message"] == "<p>User is already an owner of the channel</p>"

    
    # Allows user to invite people to private channel
    helper_test_functions.channel_invite(chicken['token'], private_cool_channel['channel_id'], bob['u_id'],_url)
    
    # Check details of channel, John, Chicken and Bob are all members,
    # John and Chicken are the only owners
    ch_details = helper_test_functions.channel_details(chicken['token'], private_cool_channel['channel_id'], _url)
    assert len(ch_details['owner_members']) == 2
    assert len(ch_details['all_members']) == 3
    assert ch_details['name'] == 'private_cool_channel'
    # Check that remove owner throw's correct exception
    response = helper_test_functions.channel_removeowner(john['token'], private_cool_channel['channel_id'], bob['u_id'], _url)
    assert response["code"] == 400
    assert response["message"] == "<p>User with u_id is not an owner of the channel</p>"


    helper_test_functions.clear(_url)

# Check channel_invite expections are working
def test_channel_invite_exceptions():
    john = helper_test_functions.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith',_url)
    bob = helper_test_functions.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime',_url)
    cool_channel = helper_test_functions.channels_create(john['token'], 'cool_channel', True,_url)


    response = helper_test_functions.channel_invite(john['token'], 9999, bob['u_id'], _url)
    assert response["code"] == 400
    assert response["message"] == "<p>Channel_id does not exist</p>"
    
    response = helper_test_functions.channel_invite(john['token'], cool_channel['channel_id'], 9999, _url)
    assert response["code"] == 400
    assert response["message"] == "<p>U_id does not exist</p>"
    
    response = helper_test_functions.channel_invite(bob['token'], cool_channel['channel_id'], john['u_id'], _url)
    assert response["code"] == 400
    assert response["message"] == "<p>Authorised user is not a member of the channel</p>"
    
    helper_test_functions.clear(_url)

# Check channel_detail expections are working
def test_channel_detail_exceptions():
    john = helper_test_functions.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith',_url)
    bob = helper_test_functions.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime',_url)
    cool_channel = helper_test_functions.channels_create(john['token'], 'cool_channel', True,_url)
    
    response = helper_test_functions.channel_details(john['token'], 9999, _url)
    assert response["code"] == 400
    assert response["message"] == "<p>Channel_id does not exist</p>"
    
    response = helper_test_functions.channel_details(bob['token'], cool_channel['channel_id'],_url)
    assert response["code"] == 400
    assert response["message"] == "<p>Authorised user is not a member of the channel</p>"

    helper_test_functions.clear(_url)

# Check channel_leave exceptions are working
def test_channel_leave_exceptions():
    john = helper_test_functions.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith',_url)
    bob = helper_test_functions.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime',_url)
    cool_channel = helper_test_functions.channels_create(john['token'], 'cool_channel', True,_url)
    
    response = helper_test_functions.channel_leave(john['token'], 9999, _url)
    assert response["code"] == 400
    assert response["message"] == "<p>Channel_id does not exist</p>"
    
    response = helper_test_functions.channel_leave(bob['token'], cool_channel['channel_id'],_url)
    assert response["code"] == 400
    assert response["message"] == "<p>Authorised user is not a member of the channel</p>"

    helper_test_functions.clear(_url)

# Check channel_leave exceptions are working
def test_channel_join_exceptions():
    john = helper_test_functions.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith',_url)
    bob = helper_test_functions.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime',_url)
    cool_channel = helper_test_functions.channels_create(john['token'], 'cool_channel', False,_url)
    
    response = helper_test_functions.channels_join(john['token'], 9999,_url)
    assert response["code"] == 400
    assert response["message"] == "<p>Channel_id does not exist</p>"
    
    response = helper_test_functions.channel_join(bob['token'], cool_channel['channel_id'], _url)
    assert response["code"] == 400
    assert response["message"] == "<p>Channel_id refers to a channel that is private </p>"
    
    helper_test_functions.clear(_url)

# Check channel_addowner exceptions are working
def test_channel_addowner_exceptions():
    john = helper_test_functions.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith',_url)
    bob = helper_test_functions.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime',_url)
    lucy = helper_test_functions.auth_register('lucy@gmail.com', 'asd123!@#', 'Lucy', 'Lime',_url)
    cool_channel = helper_test_functions.channels_create(john['token'], 'cool_channel', True,_url)
    
    response = helper_test_functions.channel_addowner(john['token'], 9999 , bob['u_id'], _url)
    assert response["code"] == 400
    assert response["message"] == "<p>Channel_id does not exist</p>"
   
    response = helper_test_functions.channel_addowner(john['token'], cool_channel['channel_id'], bob['u_id'], _url)
    assert response["code"] == 400
    assert response["message"] == "<p>User is already an owner of the channel</p>"

    response = helper_test_functions.channel_addowner(john['token'], cool_channel['channel_id'], bob['u_id'], _url)
    assert response["code"] == 400
    assert response["message"] == "<p>Authorised user is not an owner of the channel/p>"

    helper_test_functions.clear(_url)
#Check channel_removeowner exceptions are working
def test_channel_removeowner_exceptions():
    john = helper_test_functions.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith',_url)
    bob = helper_test_functions.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime',_url)
    lucy = helper_test_functions.auth_register('lucy@gmail.com', 'asd123!@#', 'Lucy', 'Lime',_url)
    cool_channel = helper_test_functions.channels_create(john['token'], 'cool_channel', True,_url)
    
    response = helper_test_functions.channel_removeowner(john['token'], 9999 , bob['u_id'], _url)
    assert response["code"] == 400
    assert response["message"] == "<p>Channel_id does not exist</p>"
    
    response = helper_test_functions.channel_removeowner(john['token'], cool_channel['channel_id'], bob['u_id'], _url)
    assert response["code"] == 400
    assert response["message"] == "<p>User with u_id is not an owner of the channel</p>"

    response = helper_test_functions.channel_removeowner(lucy['token'], cool_channel['channel_id'], john['u_id'], _url)   
    assert response["code"] == 400
    assert response["message"] == "<p>Authorised user is not an owner of the channel</p>" 


    helper_test_functions.clear(_url)


#Check channel_messages is working
def test_channel_messages():
    john = helper_test_functions.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith',_url)
    bob = helper_test_functions.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime',_url)
    cool_channel = helper_test_functions.channels_create(john['token'], 'cool_channel', False,_url)
    
    # Check exceptions
    response = helper_test_functions.channel_messages(john['token'], 9999, 0, _url)
    assert response["code"] == 400
    assert response["message"] == "<p>Channel_id does not exist</p>"
    
    response = helper_test_functions.channel_messages(john['token'], cool_channel['channel_id'], 999, _url)
    assert response["code"] == 400
    assert response["message"] == "<p>Start is greater than total number of messages</p>"
    
    response = helper_test_functions.channel_messages(bob['token'], cool_channel['channel_id'], 999, _url)
    assert response["code"] == 400
    assert response["message"] == "<p>Authorised user is not a member of the channel</p>"

    # Check that there are no messages
    messages = helper_test_functions.channel_messages(john['token'], cool_channel['channel_id'], 0)

    assert len(messages['messages']) == 0

    helper_test_functions.clear(_url)

'''

