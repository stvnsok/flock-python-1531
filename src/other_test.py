from data import data
import auth
import channel
import channels
import message
import other
from error import InputError, AccessError
from datetime import datetime

def test_clear():

    user = auth.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne')
    channels.channels_create(user['token'],"channel", True)
    
    other.clear()

    assert len(data['users']) == 0
    assert len(data['channels']) == 0

def test_users_all():

    user = auth.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne')
    token = user['token']
    auth.auth_register('jacknapier@hotmail.com', 'j0kerr', 'Jack', 'Napier')

    assert other.users_all(token) == {'users': data['users']}

def admin_userpermission_change_test():

    user = auth.auth_register('brucewayne@hotmail.com', 'b4tman', 'Bruce', 'Wayne')

    



