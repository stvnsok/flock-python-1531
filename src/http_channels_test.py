'''
26/9/2020
Purpose: Test functions in channels.py
'''
import helper_test_functions
from fixture import url as url
from data import create_token

invalid_token = create_token(999999)


def test_channels_list_no_channels(url):
    '''
    No existing channels
    '''

    response = helper_test_functions.auth_register("123@hotmail.com", "password", "Bobby", "McBob", url)
    
    response = helper_test_functions.channels_list(response["token"], url)

    assert len(response['channels']) == 0
    
    helper_test_functions.clear(url)


def test_channels_list_one(url):
    '''
    Exiting channel
    '''
    bobby = helper_test_functions.auth_register("123@hotmail.com", "password", "Bobby", "McBob",url)
    
    response = helper_test_functions.channels_create(bobby['token'], "channel_1", True, url)

    response = helper_test_functions.channels_list(bobby['token'], url)

    assert len(response['channels']) == 1
    assert response['channels'][0]['channel_id'] == 1
    assert response['channels'][0]['name'] == "channel_1"

    helper_test_functions.clear(url)

    
def test_channels_list_three(url):
    '''
    3 Existing channels
    '''

    bobby = helper_test_functions.auth_register("123@hotmail.com", "password", "Bobby", "McBob", url)

    helper_test_functions.channels_create(bobby['token'], "channel_1", True, url)
    helper_test_functions.channels_create(bobby['token'], "channel_2", False, url)
    helper_test_functions.channels_create(bobby['token'], "channel_3", True, url)
    
    response = helper_test_functions.channels_list(bobby['token'], url)
    
    assert len(response['channels']) == 3
    assert response['channels'][0]['channel_id'] == 1
    assert response['channels'][0]['name'] == "channel_1"
    
 
    assert response['channels'][1]['channel_id'] == 2
    assert response['channels'][1]['name'] == "channel_2"
    

    assert response['channels'][2]['channel_id'] == 3
    assert response['channels'][2]['name'] == "channel_3"
    
    
    helper_test_functions.clear(url)

def test_channels_list_not_in(url):
    '''
    One channel the user is not part of
    '''
    user1 = helper_test_functions.auth_register("123@hotmail.com", "password", "Bobby", "McBob", url)

    helper_test_functions.channels_create(user1['token'],"channel_1", True, url)
    user2 = helper_test_functions.auth_register("bestanime@hotmail.com", "Goku is mid!", "mei", "wei", url)

    helper_test_functions.channels_create(user2['token'],"channel_2", False, url)

    response  = helper_test_functions.channels_list(user2['token'], url)
     
    assert len(response['channels']) == 1
    assert response['channels'][0]['channel_id'] == 2
    assert response['channels'][0]['name'] == "channel_2"
    
    helper_test_functions.clear(url)
    
def test_channels_list_user_in_no_channels(url):
    '''
    User not part of any channels with existing channels
    '''
    user_1 = helper_test_functions.auth_register("123@hotmail.com", "password", "Bobby", "McBob", url)
    
    helper_test_functions.channels_create(user_1['token'],"channel_1", True, url)
    helper_test_functions.channels_create(user_1,"channel_2", False, url)
    helper_test_functions.channels_create(user_1,"channel_3", True, url)
    helper_test_functions.channels_create(user_1,"channel_4", False, url)
    user_2 = helper_test_functions.auth_register("bestanime@hotmail.com", "Goku is mid!", "mei", "wei", url)
    
    
    response = helper_test_functions.channels_list(user_2['token'], url)
    
    assert len(response['channels']) == 0
    helper_test_functions.clear(url)


#---------------------Testing channels_listall function with:------------------#

def test_channels_listall_no_channels(url):
    '''
    No existing channels
    '''
    user_1 = helper_test_functions.auth_register("123@hotmail.com", "password", "Bobby", "McBob", url)
    
    response = helper_test_functions.channels_listall(user_1['token'], url)
    assert len(response['channels']) == 0
    helper_test_functions.clear(url)

def test_channels_listall_one(url):
    '''
    1 existing channel
    '''
    user_1 = helper_test_functions.auth_register("123@hotmail.com", "password", "Bobby", "McBob", url)
    
    helper_test_functions.channels_create(user_1['token'],"channel_1", True, url)
    
    response = helper_test_functions.channels_listall(user_1['token'], url)
    
    assert len(response['channels']) == 1
    assert response['channels'][0]['channel_id'] == 1
    assert response['channels'][0]['name'] == "channel_1"
    
    helper_test_functions.clear(url) 

def test_channels_listall_three(url):
    '''
    3 Existing channels
    '''
    user_1 = helper_test_functions.auth_register("123@hotmail.com","password", "Bobby", "McBob", url)
    
    helper_test_functions.channels_create(user_1['token'],"channel_1", True, url)
    helper_test_functions.channels_create(user_1['token'],"channel_2", False, url)
    helper_test_functions.channels_create(user_1['token'],"channel_3", True, url)
    
    response = helper_test_functions.channels_listall(user_1['token'], url)
    
    assert len(response['channels']) == 3
    assert response['channels'][0]['channel_id'] == 1
    assert response['channels'][0]['name'] == "channel_1"
    
    assert response['channels'][1]['channel_id'] == 2
    assert response['channels'][1]['name'] == "channel_2"
    
    assert response['channels'][2]['channel_id'] == 3
    assert response['channels'][2]['name'] == "channel_3"
    
    helper_test_functions.clear(url) 


def test_channels_listall_not_in(url):
    '''
    One channel the user not part of
    '''
    user_1 = helper_test_functions.auth_register("123@hotmail.com", "password", "Bobby", "McBob", url)
    
    helper_test_functions.channels_create(user_1['token'],"channel_1", True, url)
    user_2 = helper_test_functions.auth_register("bestanime@hotmail.com", "Goku is mid!", "mei", "wei", url)
    
    helper_test_functions.channels_create(user_2['token'],"channel_2", False, url)
    
    response = helper_test_functions.channels_listall(user_2['token'], url)

    assert len(response['channels']) == 2
    assert response['channels'][0]['channel_id'] == 1
    assert response['channels'][0]['name'] == "channel_1"
    assert response['channels'][1]['channel_id'] == 2
    assert response['channels'][1]['name'] == "channel_2"

    helper_test_functions.clear(url)
    
def test_channels_listall_user_in_no_channels(url):
    '''
    User not part of any channels with existing channels
    '''
    user_1 = helper_test_functions.auth_register("123@hotmail.com", "password", "Bobby", "McBob", url)
    
    helper_test_functions.channels_create(user_1['token'],"channel_1", True, url)
    helper_test_functions.channels_create(user_1['token'],"channel_2", False, url)
    helper_test_functions.channels_create(user_1['token'],"channel_3", True, url)
    user_2 = helper_test_functions.auth_register("bestanime@hotmail.com", "Goku is mid!", "mei", "wei", url)
    
    response = helper_test_functions.channels_listall(user_2['token'], url)
    
    assert len(response['channels']) == 3
    assert response['channels'][0]['channel_id'] == 1
    assert response['channels'][0]['name'] == "channel_1"
    assert response['channels'][1]['channel_id'] == 2
    assert response['channels'][1]['name'] == "channel_2"
    assert response['channels'][2]['channel_id'] == 3
    assert response['channels'][2]['name'] == "channel_3"
    
    helper_test_functions.clear(url)

#--------------------Testing channels_create function for:---------------------#
def test_channels_create_invalid_name(url):
    '''
    Invalid name
    '''
    user_1 = helper_test_functions.auth_register('john@hotmail.com', 'qwe123!@#', 'John', 'Smith', url)


    error = helper_test_functions.channels_create(user_1['token'], "Hatsune Miku is best Waifu, FIGHT ME!", True, url)
    assert error['code'] == 400
    assert error['message'] == '<p>Input Channel Name too long</p>'
    helper_test_functions.clear(url)


def test_channels_create_is_public(url):
    '''
    Test new channel is public
    '''
    user_1 = helper_test_functions.auth_register('john@hotmail.com', 'qwe123!@#', 'John', 'Smith',url)
   
    helper_test_functions.channels_create(user_1['token'], "No, I'm spiderman", True, url)
    list_channels = helper_test_functions.channels_listall(user_1['token'], url)
    assert list_channels['channels'][0]['is_public'] == True
    
    helper_test_functions.channels_create(user_1['token'], "cult of spidermans", False, url)
    list_channels = helper_test_functions.channels_listall(user_1['token'], url)
    assert list_channels['channels'][1]['is_public'] == False
    helper_test_functions.clear(url)

def test_channels_create_owner(url):
    '''
    Creator got added to channel as owner
    '''
    user_1 = helper_test_functions.auth_register('john@hotmail.com', 'qwe123!@#', 'John', 'Smith', url)

    helper_test_functions.channels_create(user_1['token'], "Anime Betrayals", True, url)
    list_channels = helper_test_functions.channels_list(user_1['token'], url)

    assert list_channels['channels'][0]['members'][0]['is_owner'] == True
    helper_test_functions.clear(url)

