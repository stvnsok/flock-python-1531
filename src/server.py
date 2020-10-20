'''
imports
'''
import sys
from json import dumps
from flask import Flask, request, jsonify
# from flask_cors import CORS
from error import InputError
import auth
import channels
import channel
import user
import other

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
# CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })


'''
Auth Endpoints
'''
@APP.route("/auth/login", methods=['POST'])
def login():
    data = request.get_json()
    result = auth.auth_login(data['email'], data['password'])
    return dumps(result)

@APP.route("/auth/logout", methods=['POST'])
def logout():
    data = request.get_json()
    result = auth.auth_logout(data['token'])
    return dumps(result)

@APP.route("/auth/register", methods=['POST'])
def register():
    data = request.get_json()
    result = auth.auth_register(data['email'], data['password'], data['name_first'], data['name_last'])
    return dumps(result)


'''
Channels Endpoints
'''
@APP.route("/channels/create", methods=['POST'])
def create():
    data = request.get_json()
    result = channels.channels_create(data['token'], data['name'], data['is_public'])
    return dumps(result)

@APP.route("/channels/listall", methods=['GET'])
def listall():
    data = request.get_json()
    result = channels.channels_listall(data['token'])
    return dumps(result)

@APP.route("/channels/list", methods=['GET'])
def lists():
    data = request.get_json()
    result = channels.channels_list(data['token'])
    return dumps(result)


'''
Channel Endpoints
'''
@APP.route("/channel/invite", methods=['POST'])
def invite():
    data = request.get_json()
    result = channel.channel_invite(data['token'], data['channel_id'], data['u_id'])
    return dumps(result)

@APP.route("/channel/details", methods=['GET'])
def details():
    data = request.get_json()
    result = channel.channel_details(data['token'], data['channel_id'])
    return dumps(result)

@APP.route("/channel/messages", methods=['GET'])
def messages():
    data = request.get_json()
    result = channel.channel_messages(data['token'], data['channel_id'], data['start'])
    return dumps(result)

@APP.route("/channel/leave", methods=['POST'])
def leave():
    data = request.get_json()
    result = channel.channel_leave(data['token'], data['channel_id'])
    return dumps(result)

@APP.route("/channel/join", methods=['POST'])
def join():
    data = request.get_json()
    result = channel.channel_join(data['token'], data['channel_id'])
    return dumps(result)

@APP.route("/channel/addowner", methods=['POST'])
def addowner():
    data = request.get_json()
    result = channel.channel_addowner(data['token'], data['channel_id'], data['u_id'])
    return dumps(result)

@APP.route("/channel/removeowner", methods=['POST'])
def removeowner():
    data = request.get_json()
    result = channel.channel_removeowner(data['token'], data['channel_id'], data['u_id'])
    return dumps(result)
 

'''
User Endpoints
'''
@APP.route("/user/profile", methods=['GET'])
def profile():
    data = request.get_json()
    result = user.user_profile(data['token'], data['u_id'])
    return dumps(result)

@APP.route("/user/profile/setname", methods=['PUT'])
def setname():
    data = request.get_json()
    result = user.user_setname(data['token'], data['name_first'], data['name_last'])
    return dumps(result)

@APP.route("/user/profile/setemail", methods=['PUT'])
def setemail():
    data = request.get_json()
    result = user.user_setemail(data['token'], data['email'])
    return dumps(result)

@APP.route("/user/profile/sethandle", methods=['PUT'])
def sethandle():
    data = request.get_json()
    result = user.user_profile_sethandle(data['token'], data['handle_str'])
    return dumps(result)


'''
Message Endpoints
'''
@APP.route("/message/send", methods=['POST'])
def send():
    data = request.get_json()
    result = message.message_send(data['token'], data['channel_id'], data['message'])
    return dumps(result)

@APP.route("/message/remove", methods=['DELETE'])
def remove():
    data = request.get_json()
    result = message.message_remove(data['token'], data['message_id'])
    return dumps(result)

@APP.route("/message/edit", methods=['PUT'])
def edit():
    data = request.get_json()
    result = message.message_edit(data['token'], data['message_id'], data['message'])
    return dumps(result)

'''
Other Endpoints
'''
@APP.route("/users/all", methods=['GET'])
def usersall():
    data = request.get_json()
    result = other.users_all(data['token'])
    return dumps(result)

@APP.route("/admin/userpermission/change", methods=['POST'])
def userpermission_change():
    data = request.get_json()
    result = other.admin_userpermission_change(data['token'], data['u_id'], data['permission_id'])
    return dumps(result)

@APP.route("/search", methods=['GET'])
def search():
    data = request.get_json()
    result = other.search(data['token'], data['query_str'])
    return dumps(result)

@APP.route("/clear", methods=['DELETE'])
def clear():
    result = other.clear()
    return dumps(result)


if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port 
