#26/9/2020
#Purpose: Test functions in channels.py

import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import pytest
from data import data
import helper_test_functions

import pytest



@pytest.fixture
def _url():
    '''
    Use this fixture to get the URL of the server. It starts the server for you,
    so you don't need to.
    '''
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")


#---------------------Testing channels_list function with:---------------------#
def test_channels_list_invalid_token(_url):

  
    response = helper_test_functions.auth_register('john@hotmail.com', 'qwe123!@#', 'John', 'Smith', _url)
        
    response = helper_test_functions.channels_create(response['token'], 'channel_1', True, _url)
    
    error_response = helper_test_functions.channels_list("incorrect token", _url)

    assert error_response["code"] == 400
    assert error_response["message"] == "<p>Token is incorrect/user does not exist</p>"

    helper_test_functions.clear(_url)


def test_channels_list_no_channels(_url):
    '''
    No existing channels
    '''

    response = helper_test_functions.auth_register("123@hotmail.com", "password", "Bobby", "McBob", _url)
    new_user = response
    token = new_user['token']
    
    response = helper_test_functions.channels_list(response["token"], _url)

    assert len(response['channels']) == 0
    
    helper_test_functions.clear(_url)


def test_channels_list_one(_url):
    '''
    Exiting channel
    '''
    bobby = helper_test_functions.auth_register("123@hotmail.com", "password", "Bobby", "McBob",_url)
    
    response = helper_test_functions.channels_create(bobby['token'], "channel_1", True, _url)

    response = helper_test_functions.channels_list(bobby['token'], _url)

    assert len(response['channels']) == 1
    assert response['channels'][0]['channel_id'] == 1
    assert response['channels'][0]['name'] == "channel_1"

    helper_test_functions.clear(_url)

    

# # 3 exisiting channels
def test_channels_list_three(_url):

    
    bobby = helper_test_functions.auth_register("123@hotmail.com", "password", "Bobby", "McBob", _url)

    channel_1 = helper_test_functions.channels_create(bobby['token'], "channel_1", True, _url)
    channel_2 = helper_test_functions.channels_create(bobby['token'], "channel_2", False, _url)
    channel_3 = helper_test_functions.channels_create(bobby['token'], "channel_3", True, _url)
    
    response = helper_test_functions.channels_list(bobby['token'], _url)
    
    assert len(response['channels']) == 3
    assert response['channels'][0]['channel_id'] == 1
    assert response['channels'][0]['name'] == "channel_1"
    
 
    assert response['channels'][1]['channel_id'] == 2
    assert response['channels'][1]['name'] == "channel_2"
    

    assert response['channels'][2]['channel_id'] == 3
    assert response['channels'][2]['name'] == "channel_3"
    
    
    

# # one channel the user is not part of 
# def test_channels_list_not_in(_url):
#     user1 = helper_test_functions.auth_register("123@hotmail.com", "password", "Bobby", "McBob", _url)
#     token1 = user1['token']
#     response = helper_test_functions.channels_create(token1,"channel_1", True, _url)
#     user2 = helper_test_functions.auth_register("bestanime@hotmail.com", "Goku is mid!", "mei", "wei", _url)
#     token2 = user2['token']
#     response = helper_test_functions.channels_create(token2,"channel_2", False, _url)
    
#     error = response
#     assert error == {'channels': [
#         {'channel_id': 2, 
#         'is_public': False,
#         'members': [{
#             'is_owner': True,
#             'name_first': 'mei',
#             'name_last': 'wei',
#             'u_id': 2}],
#         'messages': [],
#         'name': 'channel_2'}],
#         }
#     requests.delete(_url + '/clear')

    
# # user not part of any channels with existing channels
# def test_channels_list_user_in_no_channels(_url):
#     user1 = helper_test_functions.auth_register("123@hotmail.com", "password", "Bobby", "McBob", _url)
#     token1 = user1['token']
#     response = helper_test_functions.channels_create(token1,"channel_1", True, _url)
#     response = helper_test_functions.channels_create(token1,"channel_2", False, _url)
#     response = helper_test_functions.channels_create(token1,"channel_3", True, _url)
#     response = helper_test_functions.channels_create(token1,"channel_4", False, _url)
#     user2 = helper_test_functions.auth_register("bestanime@hotmail.com", "Goku is mid!", "mei", "wei", _url)
#     token2 = user2['token']
    
#     error = response
#     assert error == {'channels': []}
#     requests.delete(_url + '/clear')


# #---------------------Testing channels_listall function with:------------------#
# # incorrect token
# def test_channels_listall_invalid_token(_url):
#     response = helper_test_functions.auth_register('john@hotmail.com', 'qwe123!@#', 'John', 'Smith', _url)
    
#     new_user = response
#     token = new_user['token']
    
    
#     response = helper_test_functions.channel_listall(token, _url)
    
    
#     assert error["code"] == 400
#     assert error["message"] == "<p> Token is incorrect/user does not exist</p>"

#     requests.delete(_url + '/clear')


# # no existing channels
# def test_channels_listall_no_channels(_url):
#     user= helper_test_functions.auth_register("123@hotmail.com", "password", "Bobby", "McBob", _url)
#     token = user['token']
#     error = helper_test_functions.channel_listall(token, _url)
#     assert error_response == {'channels': []}
#     requests.delete(_url + '/clear')

# # 1 exiting channel
# def test_channels_listall_one(_url):
#     response = helper_test_functions.auth_register("123@hotmail.com", "password", "Bobby", "McBob", _url)
#     token = user['token']
#     response = helper_test_functions.channels_create(token,"channel_1", True, _url)
    
    
#     response = helper_test_functions.channel_listall(token, _url)
#     error = response
#     assert error_response == {'channels': [
#         {'channel_id': 1, 
#         'is_public': True,
#         'members': [{
#             'is_owner': True,
#             'name_first': 'Bobby',
#             'name_last': 'McBob',
#             'u_id': 1}],
#         'messages': [],
#         'name': 'channel_1'}],
#         }
#     requests.delete(_url + '/clear')


# # 3 exisiting channels
# def test_channels_listall_three(_url):
#     user = helper_test_functions.auth_register("123@hotmail.com","password", "Bobby", "McBob", _url)
#     token = user['token']
#     helper_test_functions.channels_create(token,"channel_1", True, _url)
#     helper_test_functions.channels_create(token,"channel_2", False, _url)
#     helper_test_functions.channels_create(token,"channel_3", True, _url)
    
#     error_response = helper_test_functions.channel_listall(token, _url)
#     assert error_response == {'channels': [
#         {'channel_id': 1, 
#         'is_public': True,
#         'members': [{
#             'is_owner': True,
#             'name_first': 'Bobby',
#             'name_last': 'McBob',
#             'u_id': 1}],
#         'messages': [],
#         'name': 'channel_1'},
#         {'channel_id': 2,
#         'is_public': False,
#         'members': [{'is_owner': True,
#             'name_first': 'Bobby',
#             'name_last': 'McBob',
#             'u_id': 1}],
#         'messages': [],
#         'name': 'channel_2'},
#         {'channel_id': 3,
#         'is_public': True,
#         'members': [{'is_owner': True,
#             'name_first': 'Bobby',
#             'name_last': 'McBob',
#             'u_id': 1}],
#         'messages': [],
#         'name': 'channel_3'}],
#     }
#     requests.delete(_url + '/clear')

# # one channel the user is not part of 
# def test_channels_listall_not_in(_url):
#     user1 = helper_test_functions.auth_register("123@hotmail.com", "password", "Bobby", "McBob", _url)
#     token1 = user1['token']
#     helper_test_functions.channels_create(token1,"channel_1", True, _url)
#     user2 = helper_test_functions.auth_register("bestanime@hotmail.com", "Goku is mid!", "mei", "wei", _url)
#     token2 = user2['token']
#     helper_test_functions.channels_create(token2,"channel_2", False, _url)
    
#     error_response = helper_test_functions.channels_listall(token2)
#     assert error_response == {'channels': [
#         {'channel_id': 1, 
#         'is_public': True,
#         'members': [{
#             'is_owner': True,
#             'name_first': 'Bobby',
#             'name_last': 'McBob',
#             'u_id': 1}],
#         'messages': [],
#         'name': 'channel_1'},
#         {'channel_id': 2, 
#         'is_public': False,
#         'members': [{
#             'is_owner': True,
#             'name_first': 'mei',
#             'name_last': 'wei',
#             'u_id': 2}],
#         'messages': [],
#         'name': 'channel_2'}],
#         }
#     requests.delete(_url + '/clear')
    
# # user not part of any channels with existing channels
# def test_channels_listall_user_in_no_channels(_url):
#     user1 = helper_test_functions.auth_register("123@hotmail.com", "password", "Bobby", "McBob", _url)
#     token1 = user1['token']
#     helper_test_functions.channels_create(token1,"channel_1", True, _url)
#     helper_test_functions.channels_create(token1,"channel_2", False, _url)
#     helper_test_functions.channels_create(token1,"channel_3", True, _url)
#     user2 = helper_test_functions.auth_register("bestanime@hotmail.com", "Goku is mid!", "mei", "wei", _url)
#     token2 = user2['token']
    
#     error_response = helper_test_functions.channels_listall(token2)
    
#     assert error_response == {'channels': [
#         {'channel_id': 1, 
#         'is_public': True,
#         'members': [{
#             'is_owner': True,
#             'name_first': 'Bobby',
#             'name_last': 'McBob',
#             'u_id': 1}],
#         'messages': [],
#         'name': 'channel_1'},
#         {'channel_id': 2,
#         'is_public': False,
#         'members': [{'is_owner': True,
#             'name_first': 'Bobby',
#             'name_last': 'McBob',
#             'u_id': 1}],
#         'messages': [],
#         'name': 'channel_2'},
#         {'channel_id': 3,
#         'is_public': True,
#         'members': [{'is_owner': True,
#             'name_first': 'Bobby',
#             'name_last': 'McBob',
#             'u_id': 1}],
#         'messages': [],
#         'name': 'channel_3'}],
#     }

# # #--------------------Testing channels_create function for:---------------------#
# # # incorrect token
# # def test_channels_create_invalid_token(_url):
# #     user = helper_test_functions.auth_register('john@hotmail.com', 'qwe123!@#', 'John', 'Smith', _url)
# #     token = user['token']
    
    
# #     response = helper_test_functions.channels_create(token,"channel_1", True, _url)
# #     error = response
# #     assert error['code'] == 400
# #     assert error['message'] == '<p>Token is incorrect/user does not exist</p>'
# #     requests.delete(_url + '/clear')

# # # invalid name
# # def test_channels_create_invalid_name(_url):
# #     user = helper_test_functions.auth_register('john@hotmail.com', 'qwe123!@#', 'John', 'Smith', _url)
# #     token = user['token']

# #     response = helper_test_functions.channels_create(token, "Hatsune Miku is best Waifu, FIGHT ME!", True, _url)
# #     error = response
# #     assert error['code'] == 400
# #     assert error['message'] == '<p>Input Channel Name too long</p>'
# #     requests.delete(_url + '/clear')

# # # 1000 channel creation
# # def test_channels_create_lots(_url):
# #     user = helper_test_functions.auth_register('john@hotmail.com', 'qwe123!@#', 'John', 'Smith', _url)
# #     token = user['token']
# #     for no_of_channels in range(1000):
# #         channel = helper_test_functions.channels_create(token, "No, I'm spiderman", True,_url)
# #         id = channel['channel_id']
# #         assert id == (no_of_channels + 1)
# #     assert id == 1000
# #     requests.delete(_url + '/clear')

# # # correct is_public status
# # def test_channels_create_is_public(_url):
# #     user = helper_test_functions.auth_register('john@hotmail.com', 'qwe123!@#', 'John', 'Smith',_url)
# #     token = user['token']
# #     helper_test_functions.channels_create(token, "No, I'm spiderman", True, _url)
# #     list_channels = data['channels']
# #     assert list_channels[0]['is_public'] == True
# #     helper_test_functions.channels_create(token, "cult of spidermans", False, _url)
# #     assert list_channels[1]['is_public'] == False
# #     requests.delete(_url + '/clear')

# # # creator got added to channnel as owner
# # def test_channels_create_owner(_url):
# #     user = helper_test_functions.auth_register('john@hotmail.com', 'qwe123!@#', 'John', 'Smith', _url)
# #     token = user['token']
# #     helper_test_functions.channels_create(token, "Anime Betrayals", True, _url)
# #     list_channels = data['channels']
# #     assert list_channels[0]['members'][0]['is_owner'] == True
# #     requests.delete(_url + '/clear')

