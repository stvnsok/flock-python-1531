from data import data
import copy
from datetime import timezone
import calendar

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
    pass

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