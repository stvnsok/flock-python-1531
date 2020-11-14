'''
6/11/2020

'''

import pytest
import auth
import channel
import channels
import standup
from data import data, get_channel, get_user
from other import clear, search
from error import InputError, AccessError
from datetime import datetime, timedelta





######################## Tests for standup/start #############################

def test_standup_start_invalid_channel_id():
    '''
    Test for incorrect channel_id
    '''
    user_1 = auth.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob"
    )

    with pytest.raises(InputError) as e:
        standup.standup_start(user_1['token'], 909, 10)
    assert '400 Bad Request: Channel_id does not exist' == str(e.value)
    clear()



#def test_standup_start_standup_active(): 
#    '''
#    Throws an error code if there is currently an active standup running
#    '''
#    
#    user_1 = auth.auth_register(
#        "123@hotmail.com",
#        "password",
#        "Bobby",
#        "McBob"
#    )
#    new_channel = channels.channels_create(user_1['token'], 'channel_1', True)
#    channel_id = new_channel['channel_id']
#    
#    standup.standup_start(user_1['token'], channel_id, 10)
#    
#    
#    if response['channels'][0]['standup_active'] == 'True':
#        with pytest.raises(AccessError) as e:
#            standup.standup_start(user_1['token'], channel_id, 10)
#        assert 'An active standup is currently running in this channel' == str(e.value)
#
#    clear()


######################## Tests for standup/active #############################

def test_standup_active_invalid_channel_id():

    '''
    Throws an error code if the channel_id is incorrect
    '''

    user = auth.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob"    
    )
    
    with pytest.raises(InputError) as e:
        standup.standup_active(user['token'], 909)
    assert '400 Bad Request: Channel_id does not exist' == str(e.value)
    
    clear()


def test_standup_active_working(): 

    '''
    Test to stand up active is working
    '''
    user_1 = auth.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob"
    )
    
    new_channel = channels.channels_create(user_1['token'], 'channel_1', True)
    standup.standup_start(user_1['token'], new_channel['channel_id'], 10)
    response = standup.standup_active(user_1['token'], new_channel['channel_id'])
    
    assert response['is_active'] == True
    
    clear()
    



######################## Tests for standup/send #############################

def test_standup_send_invalid_channel_id():

    '''
    Throws an error code if the channel_id is incorrect
    '''
    user_1 = auth.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob"
    )
    
    channels.channels_create(user_1['token'], 'channel_1', True)
  
    message = "Hello"
    with pytest.raises(InputError) as e:
        standup.standup_send(user_1['token'], 909, message)
    assert '400 Bad Request: Channel_id does not exist' == str(e.value)
    
    clear()

def test_standup_send_unauthorised_user(): 

    '''
    Throws an error code if the user is not a member of the channel
    '''
    user_1 = auth.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob"
    )
    
    user_2 = auth.auth_register(
        "bestanime@hotmail.com",
        "Goku is mid!",
        "mei",
        "wei"
    )
    
    new_channel = channels.channels_create(user_1['token'], 'channel_1', True)
    
    standup.standup_start(user_1['token'], new_channel['channel_id'], 10)

    message = "Hello"
    

    with pytest.raises(AccessError) as e:
        standup.standup_send(user_2['token'], new_channel['channel_id'], message)
    assert '400 Bad Request: Authorised user is not a member of the channel' == str(e.value)
    clear()

# #def test_standup_send_standup_isactive(): 
# #    '''
# #    Throws an input error if there is an active standup not currently in the channel
# #    '''
# #    user_1 = helper_test_functions.auth_register(
# #        "123@hotmail.com",
# #        "password",
# #        "Bobby",
# #        "McBob"
# #        
# #    )
# #    new_channel = helper_test_functions.channels_create(user_1['token'], 'channel_1', True)
# #    channel_id = new_channel['channel_id']
# #    message = "Hello"
# #    response = helper_test_functions.standup_send(user_1['token'], channel_id, message)
# #    
# #    if response['channels'][0]['standup_active'] == 'False':
# #        assert error['code'] == 400
# #        assert error['message'] == '<p>An active standup is currently not running in this channel</p>'
    
    

def test_standup_send_invalid_length():

    '''
    Throws an input error if the message is longer than 1000 characters
    '''
    user_1 = auth.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob"
 
    )
    
    new_channel = channels.channels_create(user_1['token'], 'channel_1', True)
    channel_id = new_channel['channel_id']
    
    long_message = "But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find faultwith a man who chooses to enjoy a pleasure that has no annoying consequences,or one who avoids a pain that produces no resultant pleasure? On the other hand, we denounce"
    
    standup.standup_start(user_1['token'], new_channel['channel_id'], 10)

    with pytest.raises(InputError) as e:
        standup.standup_send(user_1['token'], channel_id, long_message + long_message)
    assert '400 Bad Request: Message is more than 1000 characters' == str(e.value)
    clear()

def test_standup_send_working(): 
    '''
    Test to check if standup_send is working
    '''
    user_1 = auth.auth_register(
        "123@hotmail.com",
        "password",
        "Bobby",
        "McBob"
    )
    
    new_channel = channels.channels_create(user_1['token'], 'channel_1', True)
    
    standup.standup_start(user_1['token'], new_channel['channel_id'], 10)
    
    msg = "hello"

    standup.standup_send(user_1['token'], new_channel['channel_id'], msg)
    
    # channel = get_channel(new_channel['channel_id'])

    handle_str = get_user(user_1['u_id'])['handle_str']

    standup_message = handle_str + ' : ' + msg

    message_sent = search(user_1['token'], standup_message)

    assert message_sent['messages'][0]['message'] == standup_message

    assert message_sent['messages'][0]['time_created'] > int(datetime.now().timestamp())
    
    clear()
