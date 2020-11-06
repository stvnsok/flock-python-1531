'''
6/11/2020

'''
import helper_test_functions
from fixture import url


######################## Tests for standup/start #############################
'''
def test_standup_start_token_incorrect(url):
    
    user_1 = helper_test_functions.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob",
        url
    )
    new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True, url)
    channel_id = new_channel['channel_id']
    
    error = helper_test_functions.standup_start(0, channel_id, 10,  url)
    assert error['code'] == 400
    assert error['message'] == '<p>Token is incorrect</p>'

    helper_test_functions.clear(url)



def test_standup_start_invalid_channel_id(url):
    user_1 = helper_test_functions.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob",
        url
    )

    
    error = helper_test_functions.standup_start(user_1['token'], 1, 10,  url)
    assert error['code'] == 400
    assert error['message'] == '<p>Channel_id does not exist</p>'

    helper_test_functions.clear(url)


def test_standup_start_invalid_length(url): 


def test_standup_start_standup_active(url): 




######################## Tests for standup/active #############################
def test_standup_active_token_incorrect(url):
    user_1 = helper_test_functions.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob",
        url
    )
    
    new_channel = helper_test_functions.channels_create(user_1['token'] 'channel_1', True, url)
    channel_id = new_channel['channel_id']
    
    error = helper_test_functions.standup_active(0, channel_id, url)
    assert error['code'] == 400
    assert error['message'] == '<p>Token is incorrect</p>'

    helper_test_functions.clear(url)


def test_standup_active_invalid_channel_id(url):

    user_1 = helper_test_functions.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob",
        url
    )
    

    error = helper_test_functions.standup_active(user_1['token'], 1, url)
    assert error['code'] == 400
    assert error['message'] == '<p>Channel_id does not exist</p>'

    helper_test_functions.clear(url)


def test_standup_active_working(url): 
    user_1 = helper_test_functions.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob",
        url
    )
    
    new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True, url)
    channel_id = new_channel['channel_id']
    
    response = helper_test_functions.standup_active(user_1['token'], channel_id, url)
    
    assert response['channels'][0]['standup_active'] == 'True'
    
    helper_test_functions.clear(url)
    



######################## Tests for standup/send #############################

def test_standup_send_token_incorrect(url): 
        
    user_1 = helper_test_functions.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob",
        url
    )
    
    new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True, url)
    channel_id = new_channel['channel_id']
    
    message = "Hello"
    response = helper_test_functions.standup_send(0, channel_id, message, url)
    assert error['code'] == 400
    assert error['message'] == '<p>Token is incorrect</p>'
    
    helper_test_functions.clear(url)

def test_standup_send_invalid_channel_id(url):
    user_1 = helper_test_functions.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob",
        url
    )
    
    new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True, url)
    channel_id = new_channel['channel_id']
    
    message = "Hello"
    response = helper_test_functions.standup_send(user_1['token'], 0, message, url)
    assert error['code'] == 400
    assert error['message'] == '<p>Channel_id does not exist</p>'
    
    helper_test_functions.clear(url)

def test_standup_send_unauthorised_user(url): 
    user_1 = helper_test_functions.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob",
        url
    )
    
    user_2 = helper_test_functions.auth_register(
        "bestanime@hotmail.com",
        "Goku is mid!",
        "mei",
        "wei",
        url
    )
    
    new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True, url)
    channel_id = new_channel['channel_id']
    
    message = "Hello"
    response = helper_test_functions.standup_send(user_2['token'], channel_id, message, url)
    assert error['code'] == 400
    assert error['message'] == '<p>Channel_id does not exist</p>'
    
    helper_test_functions.clear(url)

def test_standup_send_standup_active(url): 


def test_standup_send_working(url): 


'''
