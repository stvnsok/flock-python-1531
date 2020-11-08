'''
6/11/2020

'''
import helper_test_functions
from fixture import url


######################## Tests for standup/start #############################

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


'''

def test_standup_start_standup_active(url): 
    
    user_1 = helper_test_functions.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob",
        url
    )
    new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True, url)
    channel_id = new_channel['channel_id']
    
    helper_test_functions.standup_start(user_1['token'], channel_id, 10, url)
    
    
    if response['channels'][0]['standup_active'] == 'True':
        assert error['code'] == 400
        assert error['message'] == '<p>'An active standup is currently running in this channel'</p>'
    

    helper_test_functions.clear(url)


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
    
    assert response['is_active'] == 'True'
    
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

def test_standup_send_standup_isactive(url): 

    #Throws an input error if there is an active standup not currently in the channel
    
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
    response = helper_test_functions.standup_send(user_1['token'], channel_id, message, url)
    
    if response['channels'][0]['standup_active'] == 'False':
        assert error['code'] == 400
        assert error['message'] == '<p>'An active standup is currently not running in this channel'</p>'
    
    

def test_standup_send_invalid_length(url):

    
    #Throws an input error if the message is longer than 1000 characters
    
    user_1 = helper_test_functions.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob",
        url
    )
    
    new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True, url)
    channel_id = new_channel['channel_id']
    
    long_message = "But I must explain to you how all this mistaken idea of,
    denouncing pleasure and praising pain was born and I will give you a complete 
    account of the system, and expound the actual teachings of the great explorer 
    of the truth, the master-builder of human happiness. No one rejects, dislikes, 
    or avoids pleasure itself, because it is pleasure, but because those who do not 
    know how to pursue pleasure rationally encounter consequences that are extremely 
    painful. Nor again is there anyone who loves or pursues or desires to obtain 
    pain of itself, because it is pain, but because occasionally circumstances 
    occur in which toil and pain can procure him some great pleasure. To take a 
    trivial example, which of us ever undertakes laborious physical exercise, 
    except to obtain some advantage from it? But who has any right to find fault
    with a man who chooses to enjoy a pleasure that has no annoying consequences,
    or one who avoids a pain that produces no resultant pleasure? On the other 
    hand, we denounce"
    
    
    response = helper_test_functions.standup_send(user_1['token'], channel_id, long_message, url)
    assert error['code'] == 400
    assert error['message'] == '<p>Message is more than 1000 characters</p>'
    
    helper_test_functions.clear(url)


def test_standup_send_working(url): 
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
    response = helper_test_functions.standup_send(user_1['token'], channel_id, message, url)
    assert response['standup'][0] == {user_1['handle_str']: messages['message'] }
    
    helper_test_functions.clear(url)
'''
