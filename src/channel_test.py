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

# ######################## Tests for channel/invite #############################
# def test_channel_invite_token_incorrect(_url):
#     '''
#     This test uses the feature channel/invite with an invalid token. The
#     expected outcome is an error of 400 saying 'Token is incorrect'
#     '''
#     response = helper_test_functions.auth_register(
#         "markowong@hotmail.com",
#         "markowong",
#         "marko",
#         "wong",
#         _url
#     )
#     new_user_1 = response
#     u_id_1 = new_user_1['u_id']
#     token_1 = new_user_1['token']

#     response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
#     new_channel = response
#     channel_id = new_channel['channel_id']

#     assert channel_id == 1
#     response = helper_test_functions.channel_invite("0", channel_id, u_id_1, _url)

#     error = response
#     assert error['code'] == 400
#     assert error['message'] == '<p>Token is incorrect</p>'

#     requests.delete(_url + '/clear')

# def test_channel_invite_invalid_channel_id(_url):
#     '''
#     This test uses the feature channel/invite with an invalid channel_id. The
#     expected outcome is error of 400 saying 'Channel_id does not exist'.
#     '''
#     response = helper_test_functions.auth_register(
#         "markowong@hotmail.com",
#         "markowong",
#         "marko",
#         "wong",
#         _url
#     )
#     new_user_1 = response
#     token_1 = new_user_1['token']

#     response = helper_test_functions.auth_register(
#         "markowong2@hotmail.com",
#         "markowong2",
#         "marko2",
#         "wong2",
#         _url
#     )
#     new_user_2 = response
#     u_id_2 = new_user_2['u_id']

#     response = helper_test_functions.channel_invite(token_1, 0, u_id_2, _url)
#     error = response
#     assert error['code'] == 400
#     assert error['message'] == '<p>Channel_id does not exist</p>'
#     requests.delete(_url + '/clear')

# def test_channel_invite_invalid_user_id(_url):
#     '''
#     This test uses the feature channel/invite with an invalid user_id. The
#     expected outcome is error of 400 saying 'user_id does not exist'.
#     '''
#     response = helper_test_functions.auth_register(
#         "markowong@hotmail.com",
#         "markowong",
#         "marko",
#         "wong",
#         _url
#     )
#     new_user_1 = response
#     token_1 = new_user_1['token']

#     response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
#     new_channel = response
#     channel_id = new_channel['channel_id']

#     response = helper_test_functions.channel_invite(token_1, channel_id, 2, _url)
#     error = response
#     assert error['code'] == 400
#     assert error['message'] == '<p>user_id does not exist</p>'
#     requests.delete(_url + '/clear')

# def test_channel_invite_user_not_in_channel(_url):
#     '''
#     This test uses the feature channel/invite with an user_id that is already in
#     the channel. The expected outcome is error of 400 saying 'Authorised user is
#     not a member of the channel'.
#     '''
#     response = helper_test_functions.auth_register(
#         "markowong@hotmail.com",
#         "markowong",
#         "marko",
#         "wong",
#         _url
#     )
#     new_user_1 = response
#     token_1 = new_user_1['token']

#     response = helper_test_functions.auth_register(
#         "markowong2@hotmail.com",
#         "markowong2",
#         "marko2",
#         "wong2",
#         _url
#     )
#     new_user_2 = response
#     token_2 = new_user_2['token']

#     response = helper_test_functions.auth_register(
#         "markowong3@hotmail.com",
#         "markowong3",
#         "marko3",
#         "wong3",
#         _url
#     )
#     new_user_3 = response
#     u_id_3 = new_user_3['u_id']

#     response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
#     new_channel = response
#     channel_id = new_channel['channel_id']

#     response = helper_test_functions.channel_invite(token_2, channel_id, u_id_3, _url)
#     error = response
#     assert error['code'] == 400
#     assert error['message'] == '<p>Authorised user is not a member of the channel</p>'
#     requests.delete(_url + '/clear')


# def test_channel_invite_working(_url):
#     '''
#     This test uses the feature channel/invite with valid inputs. The expected
#     utcome is the invited user is added to the channel immediately.
#     '''
#     response = helper_test_functions.auth_register(
#         "markowong@hotmail.com",
#         "markowong",
#         "marko",
#         "wong",
#         _url
#     )
#     new_user_1 = response
#     token_1 = new_user_1['token']

#     response = helper_test_functions.auth_register(
#         "markowong2@hotmail.com",
#         "markowong2",
#         "marko2",
#         "wong2",
#         _url
#     )
#     new_user_2 = response
#     token_2 = new_user_2['token']
#     u_id_2 = new_user_2['u_id']

#     response = helper_test_functions.auth_register(
#         "markowong3@hotmail.com",
#         "markowong3",
#         "marko3",
#         "wong3",
#         _url
#     )
#     new_user_3 = response
#     u_id_3 = new_user_3['u_id']

#     response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
#     new_channel = response
#     channel_id = new_channel['channel_id']

#     # invite users to channel
#     helper_test_functions.channel_invite(token_1, channel_id, u_id_2, _url)
#     helper_test_functions.channel_invite(token_2, channel_id, u_id_3, _url)

#     # check that the users are in the channel
#     response = helper_test_functions.channels_list(token_1, _url)
#     memebers = response['channels'][0]['members']
#     assert memebers[0]['name_first'] == 'marko'
#     assert memebers[1]['name_first'] == 'marko2'
#     assert memebers[2]['name_first'] == 'marko3'

# ######################### Tests for channel/details ############################
# def test_channel_details_invalid_token(_url):
#     '''
#     This test uses the feature channel/details with an invalid token. The
#     expected outcome is an error of 400 saying 'Token is incorrect'
#     '''
#     response = helper_test_functions.auth_register(
#         "markowong@hotmail.com",
#         "markowong",
#         "marko",
#         "wong",
#         _url
#     )
#     new_user_1 = response
#     token_1 = new_user_1['token']

#     response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
#     new_channel = response
#     channel_id = new_channel['channel_id']

#     response = helper_test_functions.channel_details("0", channel_id, _url)

#     error = response
#     assert error['code'] == 400
#     assert error['message'] == '<p>Token is incorrect</p>'

#     requests.delete(_url + '/clear')

# def test_channel_details_invalid_channel_id(_url):
#     '''
#     This test uses the feature channel/details with an invalid channel_id. The
#     expected outcome is an error of 400 saying 'Channel_id does not exist'
#     '''
#     response = helper_test_functions.auth_register(
#         "markowong@hotmail.com",
#         "markowong",
#         "marko",
#         "wong",
#         _url
#     )
#     new_user_1 = response
#     token_1 = new_user_1['token']

#     response = helper_test_functions.channel_details(token_1, 1, _url)

#     error = response
#     assert error['code'] == 400
#     assert error['message'] == '<p>Channel_id does not exist</p>'

#     requests.delete(_url + '/clear')

# def test_channel_details_user_not_a_member(_url):
#     '''
#     This test uses the feature channel/detials with an user_id that is not in
#     the channel. The expected outcome is error of 400 saying 'Authorised user is
#     not a member of the channel'.
#     '''
#     response = helper_test_functions.auth_register(
#         "markowong@hotmail.com",
#         "markowong",
#         "marko",
#         "wong",
#         _url
#     )
#     new_user_1 = response
#     token_1 = new_user_1['token']

#     response = helper_test_functions.auth_register(
#         "markowong2@hotmail.com",
#         "markowong2",
#         "marko2",
#         "wong2",
#         _url
#     )
#     new_user_2 = response
#     token_2 = new_user_2['token']

#     response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
#     new_channel = response
#     channel_id = new_channel['channel_id']

#     response = helper_test_functions.channel_details(token_2, channel_id, _url)
#     error = response
#     assert error['code'] == 400
#     assert error['message'] == '<p>Authorised user is not a member of the channel</p>'
#     requests.delete(_url + '/clear')

# def test_channel_detail_working(_url):
#     '''
#     This test uses the feature channel/detials with valid inputs. The expected
#     outcome is providing basic details about the channel including: name,
#     owner_members, all_members.
#     '''
#     response = helper_test_functions.auth_register(
#         "markowong@hotmail.com",
#         "markowong",
#         "marko",
#         "wong",
#         _url
#     )
#     new_user_1 = response
#     token_1 = new_user_1['token']

#     response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
#     new_channel = response
#     channel_id = new_channel['channel_id']

#     response = helper_test_functions.channel_details(token_1, channel_id, _url)
#     assert response['owner_members'][0]['name_first'] == 'marko'
#     assert response['all_members'][0]['name_first'] == 'marko'

# ######################### Tests for channel/messages ###########################
# def test_channel_messages_invalid_token(_url):
#     '''
#     This test uses the feature channel/messages with an invalid token. The
#     expected outcome is an error of 400 saying 'Token is incorrect'
#     '''
#     response = helper_test_functions.auth_register(
#         "markowong@hotmail.com",
#         "markowong",
#         "marko",
#         "wong",
#         _url
#     )
#     new_user_1 = response
#     token_1 = new_user_1['token']

#     response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
#     new_channel = response
#     channel_id = new_channel['channel_id']

#     error = helper_test_functions.channel_messages("incorrect_token", channel_id, 0, _url)

#     assert error['code'] == 400
#     assert error['message'] == '<p>Token is incorrect</p>'

#     requests.delete(_url + '/clear')

# def test_channel_messages_invalid_channel_id(_url):
#     '''
#     This test uses the feature channel/messages with an invalid channel_id. The
#     expected outcome is an error of 400 saying 'Channel_id does not exist'
#     '''

#     user_1 = helper_test_functions.auth_register(
#         "123@hotmail.com", 
#         "password", 
#         "Bobby", 
#         "McBob",
#         _url
#     )
   
#     new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True, _url)

#     error = helper_test_functions.channel_messages(user_1['token'], 1000, 0, _url)

#     assert error['code'] == 400
#     assert error['message'] == '<p>Channel_id does not exist</p>'
    
#     requests.delete(_url + '/clear')

# def test_channel_messages_start_greater(_url): #NOT DONE
#     '''
#     This test uses the feature channel/messages with an invalid start. The
#     expected outcome is an error of 400 saying 'Start is greater than total
#     number of messages'.
#     '''

#     user_1 = helper_test_functions.auth_register(
#         "123@hotmail.com", 
#         "password", 
#         "Bobby", 
#         "McBob",
#         _url
#     )
   
#     new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True, _url)

#     all_channels = helper_test_functions.channels_listall(user_1['token'], _url)

#     error = helper_test_functions.channel_messages(user_1['token'], new_channel['channel_id'], 100, _url)
    
#     assert error['code'] == 400
#     assert error['message'] == '<p>Start is greater than total number of messages</p>'
#     requests.delete(_url + '/clear')
    
    
# def test_channel_messages_user_not_a_member(_url): #NOT DONE
#     '''
#     This test uses the feature channel/messages with an user_id that is not in
#     the channel. The expected outcome is error of 400 saying 'Authorised user is
#     not a member of the channel'.
#     '''

#     user_1 = helper_test_functions.auth_register(
#         "markowong2@hotmail.com",
#         "markowong2",
#         "marko2",
#         "wong2",
#         _url
#     )

    
#     user_2 = helper_test_functions.auth_register(
#         "markowong@hotmail.com",
#         "markowong",
#         "marko",
#         "wong",
#         _url
#     )

#     new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True, _url)

#     response = helper_test_functions.channel_messages(user_2['token'], new_channel['channel_id'],0, _url)
#     error = response
#     assert error['code'] == 400
#     assert error['message'] == '<p>Authorised user is not a member of the channel</p>'
#     requests.delete(_url + '/clear')

# def test_channel_messages(_url):
#     '''
#     This test uses the feature channel/messages to confirm
#     all messages sent are stored correctly. 
#     The expected outcome is dictories of messages, start, end.
#     '''

#     user_1 = helper_test_functions.auth_register(
#         "markowong2@hotmail.com",
#         "markowong2",
#         "marko2",
#         "wong2",
#         _url
#     )

#     new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True, _url)

#     for i in range(20):
#         helper_test_functions.message_send(user_1['token'], new_channel['channel_id'], "Hello" ,_url)
    

#     response = helper_test_functions.channel_messages(user_1['token'], new_channel['channel_id'], 0, _url)
    
#     assert response['end'] == -1
    
#     for message in response['messages']:
#         assert message['message'] == "Hello"
    
#     for i in range(100):
#         helper_test_functions.message_send(user_1['token'], new_channel['channel_id'], "Goodbye" ,_url)
    
#     response = helper_test_functions.channel_messages(user_1['token'], new_channel['channel_id'], 20, _url)
    
#     assert response['end'] == 70
    
#     for message in response['messages']:
#         assert message['message'] == "Goodbye"

#     helper_test_functions.clear(_url)



# ########################## Tests for channel/leave #############################
# def test_channel_leave_invalid_token(_url):
#     '''
#     This test uses the feature channel/leave with an invalid token. The
#     expected outcome is an error of 400 saying 'Token is incorrect'
#     '''
#     response = helper_test_functions.auth_register(
#         "markowong@hotmail.com",
#         "markowong",
#         "marko",
#         "wong",
#         _url
#     )
#     new_user_1 = response
#     token_1 = new_user_1['token']

#     response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
#     new_channel = response
#     channel_id = new_channel['channel_id']

#     response = helper_test_functions.channel_leave("0", channel_id, _url)

#     error = response
#     assert error['code'] == 400
#     assert error['message'] == '<p>Token is incorrect</p>'

#     requests.delete(_url + '/clear')

# def test_channel_leave_invalid_channel_id(_url):
#     '''
#     This test uses the feature channel/leave with an invalid channel_id. The
#     expected outcome is an error of 400 saying 'Channel_id does not exist'
#     '''

#     user_1 = helper_test_functions.auth_register(
#         "123@hotmail.com",
#         "password",
#         "Bobby",
#         "McBob",
#         _url
#     )

#     error = helper_test_functions.channel_leave(user_1['token'], 1, _url)
#     assert error['code'] == 400
#     assert error['message'] == '<p>Channel_id does not exist</p>'

#     helper_test_functions.clear(_url)

# def test_channel_leave_user_not_a_member(_url):
#     '''
#     This test uses the feature channel/leave with an user_id that is not in
#     the channel. The expected outcome is error of 400 saying 'Authorised user is
#     not a member of the channel'.
#     '''
#     user_1 = helper_test_functions.auth_register(
#         "123@hotmail.com",
#         "password",
#         "Bobby",
#         "McBob",
#         _url
#     )
#     new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True, _url)

#     user_2 = helper_test_functions.auth_register(
#         "bestanime@hotmail.com",
#         "Goku is mid!",
#         "mei",
#         "wei",
#         _url
#     )
#     channel_id = new_channel['channel_id']

#     error = helper_test_functions.channel_leave(user_2['token'], channel_id, _url)
#     assert error['code'] == 400
#     assert error['message'] == '<p>Authorised user is not a member of the channel</p>'

#     helper_test_functions.clear(_url)

# def test_channel_leave_working(_url):
#     '''
#     This test uses the feature channel/leave with valid inputs. The expected
#     outcome is that the database removes that user from the list of members for
#     that channel.
#     '''

#     response = helper_test_functions.auth_register(
#         "123@hotmail.com",
#         "password",
#         "Bobby",
#         "McBob",
#         _url
#     )
#     new_user_1 = response
#     token_1 = new_user_1['token']
#     new_channel = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
#     channel_id = new_channel['channel_id']

#     response = helper_test_functions.auth_register(
#         "markowong2@hotmail.com",
#         "markowong2",
#         "marko2",
#         "wong2",
#         _url
#     )
#     new_user_2 = response
#     token_2 = new_user_2['token']
#     u_id_2 = new_user_2['u_id']


#     helper_test_functions.channel_invite(token_1, channel_id, u_id_2, _url)
#     helper_test_functions.channel_leave(token_2, channel_id, _url)

#     response = helper_test_functions.channel_details(token_1, channel_id, _url)
#     assert len(response['all_members']) == 1

#     helper_test_functions.clear(_url)

# ########################### Tests for channel/join #############################
# def test_channel_join_invalid_token(_url):
#     '''
#     This test uses the feature channel/join with an invalid token. The
#     expected outcome is an error of 400 saying 'Token is incorrect'
#     '''
#     response = helper_test_functions.auth_register(
#         "markowong@hotmail.com",
#         "markowong",
#         "marko",
#         "wong",
#         _url
#     )
#     new_user_1 = response
#     token_1 = new_user_1['token']

#     response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
#     new_channel = response
#     channel_id = new_channel['channel_id']

#     response = helper_test_functions.channel_join("0", channel_id, _url)

#     error = response
#     assert error['code'] == 400
#     assert error['message'] == '<p>Token is incorrect</p>'

#     requests.delete(_url + '/clear')

# def test_channel_join_invalid_channel_id(_url): 
#     '''
#     This test uses the feature channel/join with an invalid channel_id. The
#     expected outcome is an error of 400 saying 'Channel_id does not exist'
#     '''
#     response = helper_test_functions.auth_register(
#         "markowong@hotmail.com",
#         "markowong",
#         "marko",
#         "wong",
#         _url
#     )
#     new_user_1 = response
#     token_1 = new_user_1['token']

#     response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)

#     response = helper_test_functions.channel_join(token_1, 909, _url)

#     error = response
#     assert error['code'] == 400
#     assert error['message'] == '<p>Channel_id does not exist</p>'

#     requests.delete(_url + '/clear')

# def test_channel_join_user_not_a_member(_url):
#     '''
#     This test uses the feature channel/join with an user_id that is not in
#     the channel. The expected outcome is error of 400 saying 'Channel_id refers
#     to a channel that is private
#     '''

#     user_1 = helper_test_functions.auth_register(
#         "123@hotmail.com",
#         "password",
#         "Bobby",
#         "McBob",
#         _url
#     )
#     new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', False, _url)

#     user_2 = helper_test_functions.auth_register(
#         "bestanime@hotmail.com",
#         "Goku is mid!",
#         "mei",
#         "wei",
#         _url
#     )
#     channel_id = new_channel['channel_id']

#     error = helper_test_functions.channel_join(user_2['token'], channel_id, _url)
#     assert error['code'] == 400
#     assert error['message'] == '<p>Channel_id refers to a channel that is private</p>'

#     helper_test_functions.clear(_url)

# def test_channel_join_working(_url):
#     '''
#     This test uses the feature channel/join with valid inputs. The expected
#     outcome is that the database adds that user to the list of members for that
#     public channel.
#     '''
#     response = helper_test_functions.auth_register(
#         "123@hotmail.com",
#         "password",
#         "Bobby",
#         "McBob",
#         _url
#     )
#     new_user_1 = response
#     token_1 = new_user_1['token']
#     new_channel = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
#     channel_id = new_channel['channel_id']

#     response = helper_test_functions.auth_register(
#         "markowong2@hotmail.com",
#         "markowong2",
#         "marko2",
#         "wong2",
#         _url
#     )
#     new_user_2 = response
#     token_2 = new_user_2['token']

#     helper_test_functions.channel_join(token_2, channel_id, _url)

#     response = helper_test_functions.channel_details(token_1, channel_id, _url)
#     assert len(response['all_members']) == 2

#     helper_test_functions.clear(_url)

# ######################## Tests for channel/addowner ############################
# def test_channel_addowner_invalid_token(_url):
#     '''
#     This test uses the feature channel/addowner with an invalid token. The
#     expected outcome is an error of 400 saying 'Token is incorrect'
#     '''
#     response = helper_test_functions.auth_register(
#         "markowong@hotmail.com",
#         "markowong",
#         "marko",
#         "wong",
#         _url
#     )
#     new_user_1 = response
#     u_id_1 = new_user_1['token']
#     token_1 = new_user_1['token']

#     response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
#     new_channel = response
#     channel_id = new_channel['channel_id']

#     response = helper_test_functions.channel_addowner("0", channel_id, u_id_1, _url)

#     error = response
#     assert error['code'] == 400
#     assert error['message'] == '<p>Token is incorrect</p>'

#     requests.delete(_url + '/clear')

# def test_channel_addowner_invalid_channel_id(_url): 
#     '''
#     This test uses the feature channel/addowner with an invalid channel_id. The
#     expected outcome is an error of 400 saying 'Channel_id does not exist'
#     '''
#     response = helper_test_functions.auth_register(
#         "markowong@hotmail.com",
#         "markowong",
#         "marko",
#         "wong",
#         _url
#     )
#     new_user_1 = response
#     u_id_1 = new_user_1['token']
#     token_1 = new_user_1['token']

#     response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)

#     response = helper_test_functions.channel_addowner(token_1, 909, u_id_1, _url)

#     error = response
#     assert error['code'] == 400
#     assert error['message'] == '<p>Channel_id does not exist</p>'

#     requests.delete(_url + '/clear')

# def test_channel_addowner_user_not_a_member(_url):
#     '''
#     This test uses the feature channel/addowner with an user_id that is not in
#     the channel. The expected outcome is error of 400 saying 'Authorised user is
#     not an owner of the channel'.
#     '''

#     user_1 = helper_test_functions.auth_register(
#         "123@hotmail.com",
#         "password",
#         "Bobby",
#         "McBob",
#         _url
#     )
#     new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True, _url)

#     user_2 = helper_test_functions.auth_register(
#         "bestanime@hotmail.com",
#         "Goku is mid!", 
#         "mei", 
#         "wei", 
#         _url
#     )
#     channel_id = new_channel['channel_id']

#     error = helper_test_functions.channel_addowner(user_2['token'], channel_id, user_2['u_id'], _url)
#     assert error['code'] == 400
#     assert error['message'] == '<p>Authorised user is not an owner of the channel</p>'

#     requests.delete(_url + '/clear')

def test_channel_addowner_working(_url): #NOT DONE
    '''
    This test uses the feature channel/addowner with valid inputs. The expected
    outcome is that the database adds that user to the list of owner_members for
    that channel.
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

    helper_test_functions.channel_addowner(user_1['token'], channel_id, user_2['u_id'], _url)
    
    channel_details = helper_test_functions.channel_details(user_2['token'], channel_id, _url)

    assert channel_details['owner_members'][0]['u_id'] == user_1['u_id']
    assert channel_details['owner_members'][1]['u_id'] == user_2['u_id']

    requests.delete(_url + '/clear')

####################### Tests for channel/removeowner ##########################

# def test_channel_removeowner_invalid_token(_url): 
#     '''
#     This test uses the feature channel/removeowner with an invalid token. The
#     expected outcome is an error of 400 saying 'Token is incorrect'
#     '''

#     response = helper_test_functions.auth_register(
#         "markowong@hotmail.com",
#         "markowong",
#         "marko",
#         "wong",
#         _url
#     )
#     new_user_1 = response
#     u_id_1 = new_user_1['token']
#     token_1 = new_user_1['token']

#     response = helper_test_functions.channels_create(token_1, 'channel_1', True, _url)
#     new_channel = response
#     channel_id = new_channel['channel_id']

#     response = helper_test_functions.channel_removeowner("0", channel_id, u_id_1, _url)

#     error = response
#     assert error['code'] == 400
#     assert error['message'] == '<p>Token is incorrect</p>'

#     requests.delete(_url + '/clear')

# def test_channel_removeowner_invalid_channel_id(_url): 
#     '''
#     This test uses the feature channel/removeowner with an invalid channel_id. The
#     expected outcome is an error of 400 saying 'Channel_id does not exist'
#     '''
   
#     user_1 = helper_test_functions.auth_register(
#         "123@hotmail.com", 
#         "password", 
#         "Bobby", 
#         "McBob",
#         _url
#     )
    
#     user_2 = helper_test_functions.auth_register(
#         "bestanime@hotmail.com",
#         "Goku is mid!", 
#         "mei", 
#         "wei", 
#         _url
#     )
#     channel_1 = helper_test_functions.channels_create(user_1['token'], "channel_1", True, _url)
#     helper_test_functions.channel_addowner(user_1['token'], channel_1['channel_id'], user_2['u_id'],_url)
    
#     response = helper_test_functions.channel_removeowner(user_1['token'], 909, user_2['u_id'],_url)

#     assert response["code"] == 400
#     assert response["message"] == '<p>Channel_id does not exist</p>'
#     requests.delete(_url + '/clear')
    
# def test_channel_removeowner_user_not_a_member(_url):  
#     '''
#     This test uses the feature channel/removeowner with an user_id that is not in
#     the channel. The expected outcome is error of 400 saying 'Authorised user is
#     not an owner of the channel'.
#     '''
    
#     user_1 = helper_test_functions.auth_register(
#         "123@hotmail.com", 
#         "password", 
#         "Bobby", 
#         "McBob",
#         _url
#     )
#     new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True, _url)
    
#     user_2 = helper_test_functions.auth_register(
#         "bestanime@hotmail.com",
#         "Goku is mid!", 
#         "mei", 
#         "wei", 
#         _url
#     )
#     channel_id = new_channel['channel_id']

#     error = helper_test_functions.channel_removeowner(user_2['token'], channel_id, user_2['u_id'], _url)
#     assert error['code'] == 400
#     assert error['message'] == '<p>Authorised user is not an owner of the channel</p>'
    
#     helper_test_functions.clear(_url)

def test_channel_removeowner_working(_url): #NOT DONE
    '''
    This test uses the feature channel/removeowner with valid inputs. The expected
    outcome is that the database removes that user from the list of owners_members
    for that channel.
    '''






