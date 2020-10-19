from data import data
import copy
from datetime import timezone
import calendar
from error import InputError, AccessError

def clear():
    data['users'].clear()
    data['channels'].clear()
    data['messages'].clear()


def users_all(token):
    '''
    Returns a list of all users and their associated details
    '''
    return {
        'users': data['users'],
    }

def admin_userpermission_change(token, u_id, permission_id):
    '''
    Given a User by their user ID, set their permissions to new permissions described by permission_id
    '''
    user = data['users']
    
    # Validate permission_id is correct
    if permission_id != 1 or permission_id != 2:
        raise InputError('Permission_id does not refer to a value permission')
    
    # Get Authorised user
    authorised_user = next(user for user in users if user['token'] == token, None)
    
    # Check authorised user permission is 1
    if authorised_user['permission_id'] != 1:
        raise InputError('The authorised user is not an admin or owner')

    # Get selected user 
    selected_user = next(user for user in users if user['u_id'] == u_id, None)

    # Check if u_id refers to valid user
    if selected_user is None:
        raise InputError('U_id does not refer to a valid user')

    # Set permission id
    selected_user['permission_id'] = permission_id

    return {}

    
def search(token, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }

def get_timestamp():
    '''
    Returns a unix timestamp
    '''
    d = datetime.utcnow()
    return calendar.timegm(d.utctimetuple())

def check(email):
    '''
    Checks that the entered email is valid based on regex expression
    '''
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    # Make a regular expression for validating an Email
    if re.search(regex, email):
        return True

    return False