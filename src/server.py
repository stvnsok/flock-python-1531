'''
imports
'''
import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
import auth
import channels
import channel
import user_marko

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
CORS(APP)

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

@APP.route("/auth/login", methods=['POST'])
def login():
    return(auth.auth_login())

@APP.route("/auth/logout", methods=['POST'])
def logout():
    return(auth.auth_logout())

@APP.route("/auth/register", methods=['POST'])
def register():
    return(auth.auth_register())

@APP.route("/channels/create", methods=['POST'])
def create():
    return(channels.channels_create())

@APP.route("/channels/listall", methods=['GET'])
def listall():
    return(dumps(channels.channels_listall()))

@APP.route("/channels/list", methods=['GET'])
def lists():
    return(dumps(channels.channels_list()))

@APP.route("/channel/invite", methods=['POST'])
def invite():
    return(channel.channel_invite())

@APP.route("/channel/details", methods=['GET'])
def details():
    return(dumps(channel.channel_details()))

@APP.route("/channel/messages", methods=['GET'])
def messages():
    return(dumps(channel.channel_messages()))

@APP.route("/channel/leave", methods=['POST'])
def leave():
    return(channel.channel_leave())

@APP.route("/channel/join", methods=['POST'])
def join():
    return(channel.channel_join())

@APP.route("/channel/addowner", methods=['POST'])
def addowener():
    return(channel.channel_addowner())

@APP.route("/channel/removeowner", methods=['POST'])
def removeowener():
    return(channel.channel_removeowner())

@APP.route("/user/profile", methods=['GET'])
def profile():
    return(user_marko.user_profile())

@APP.route("/user/profile/sethandle", methods=['PUT'])
def sethandle():
    return(user_marko.user_profile_sethandle())

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port 
