'''
Tests for user.py

'''

import user
from error import InputError, AccessError
from other import clear
from data import data
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
import pytest
import server
import helper_test_functions

# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

'''
Tests for user/profile
'''
def test_profile_invalid_user_token(url):
    # register first user
    response = requests.post(url + 'auth/register', json={
        "email": "markowong@hotmail.com", 
        "password": "markowong",
        "name_first": "marko",
        "name_last": "wong",
    })
    new_user = response.json()
    u_id = new_user["u_id"]
    
    # input invalid token into user/profile
    response = requests.get(url + 'user/profile', json={"token": "invalid_token", "u_id": u_id})
    error = response.json()
    assert error['code'] == 400
    assert error['message'] == '<p>Token is incorrect</p>'

    # clears data
    requests.delete(url + '/clear')

def test_profile_U_id_not_found(url):
    # register first user
    response = requests.post(url + 'auth/register', json={
        "email": "markowong@hotmail.com", 
        "password": "markowong",
        "name_first": "marko",
        "name_last": "wong",
    })
    new_user = response.json()
    # u_id = new_user['u_id']
    token = new_user['token']

    #request an invalid u_id
    response = requests.get(url + 'user/profile', json={"token": token, "u_id": 2})
    error = response.json()
    assert error['code'] == 400
    assert error['message'] == '<p>No users with the entered u_id was found</p>'

    # clears data
    requests.delete(url + '/clear')

def test_profile_display_correct_info(url):
    # register first user
    response = requests.post(url + 'auth/register', json={
        "email": "markowong@hotmail.com", 
        "password": "markowong",
        "name_first": "marko",
        "name_last": "wong",
    })
    new_user = response.json()
    u_id = new_user['u_id']
    token = new_user['token']

    # display profile of the caller
    response = requests.get(url + 'user/profile', json={"token": token, "u_id": u_id})
    profile = response.json()
    assert profile['u_id'] == u_id
    assert profile['email'] == "markowong@hotmail.com"
    assert profile['name_first'] == "marko"
    assert profile['name_last'] == "wong"
    assert profile['handle_str'] == "markowong"

    # register second user
    response = requests.post(url + 'auth/register', json={
        "email": "markowong2@hotmail.com", 
        "password": "markowong",
        "name_first": "marko2",
        "name_last": "wong2",
    })
    new_user = response.json()
    u_id = new_user['u_id']

    # display profile of another user called from the first user
    response = requests.get(url + 'user/profile', json={"token": token, "u_id": u_id})
    profile = response.json()
    assert profile['u_id'] == u_id
    assert profile['email'] == "markowong2@hotmail.com"
    assert profile['name_first'] == "marko2"
    assert profile['name_last'] == "wong2"
    assert profile['handle_str'] == "marko2wong2"

    # clears data
    requests.delete(url + '/clear')

'''
Tests for user/profile/sethandle
'''
def test_profile_handle_invalid_user_token(url):
    # register first user
    response = requests.post(url + 'auth/register', json={
        "email": "markowong@hotmail.com", 
        "password": "markowong",
        "name_first": "marko",
        "name_last": "wong",
    })
    new_user = response.json()
    # u_id = new_user['u_id']
    
    # input invalid token into user/profile/sethandle
    response = requests.put(url + 'user/profile/sethandle', json={"token": "invalid_token", "handle_str": "Mr.cool"})
    error = response.json()
    assert error['code'] == 400
    assert error['message'] == '<p>Token is incorrect</p>'

    # clears data
    requests.delete(url + '/clear')

def test_profile_handle_too_short(url):
    # register first user
    response = requests.post(url + 'auth/register', json={
        "email": "markowong@hotmail.com", 
        "password": "markowong",
        "name_first": "marko",
        "name_last": "wong",
    })
    new_user = response.json()
    # u_id = new_user['u_id']
    token = new_user['token']

    # input invalid handle into user/profile/sethandle
    response = requests.put(url + 'user/profile/sethandle', json={"token": token, "handle_str": "Mr"})
    error = response.json()
    assert error['code'] == 400
    assert error['message'] == '<p>Handle length needs to be between 3 and 20</p>'

    # clears data
    requests.delete(url + '/clear')


def test_profile_handle_too_long(url):
    # register first user
    response = requests.post(url + 'auth/register', json={
        "email": "markowong@hotmail.com", 
        "password": "markowong",
        "name_first": "marko",
        "name_last": "wong",
    })
    new_user = response.json()
    # u_id = new_user['u_id']
    token = new_user['token']

    # input invalid handle into user/profile/sethandle
    response = requests.put(url + 'user/profile/sethandle', json={"token": token, "handle_str": "soo...how is your day"})
    error = response.json()
    assert error['code'] == 400
    assert error['message'] == '<p>Handle length needs to be between 3 and 20</p>'

    # clears data
    requests.delete(url + '/clear')

def test_profile_handle_exisiting(url):
    # register first user
    response = requests.post(url + 'auth/register', json={
        "email": "markowong@hotmail.com", 
        "password": "markowong",
        "name_first": "marko",
        "name_last": "wong",
    })
    new_user = response.json()
    u_id = new_user['u_id']
    token = new_user['token']

    # input valid handle_str into user/profile
    requests.put(url + 'user/profile/sethandle', json={"token": token, "handle_str": "10/10?"})
    for user in data['users']:
        if user['u_id'] == u_id:
            assert user['handle_str'] == "10/10?"

    # register second user
    response = requests.post(url + 'auth/register', json={
        "email": "markowong2@hotmail.com", 
        "password": "markowong2",
        "name_first": "marko2",
        "name_last": "wong2",
    })
    new_user = response.json()
    u_id = new_user['u_id']
    token = new_user['token']
        
    # input a valid duplicate handle_str into user/profile
    response = requests.put(url + 'user/profile/sethandle', json={"token": token, "handle_str": "10/10?"})
    error = response.json()
    assert error['code'] == 400
    assert error['message'] == '<p>Handle already in use by another user</p>'

    # clears data
    requests.delete(url + '/clear')

def test_profile_handle_correct_update(url):
    # register first user
    response = requests.post(url + 'auth/register', json={
        "email": "markowong@hotmail.com", 
        "password": "markowong",
        "name_first": "marko",
        "name_last": "wong",
    })
    new_user = response.json()
    u_id = new_user['u_id']
    token = new_user['token']

    # input valid handle_str into user/profile
    requests.put(url + 'user/profile/sethandle', json={"token": token, "handle_str": "10/10?"})
    for user in data['users']:
        if user['u_id'] == u_id:
            assert user['handle_str'] == "10/10?"

    # clears data
    requests.delete(url + '/clear')


def test_name_incorrect_length(url):
    # register first user
    payload = helper_test_functions.register_user("brucewayne@hotmail.com", "batm4n", "bruce", "wayne", url)
    new_user = payload
    token = new_user['token']
    
    response = helper_test_functions.user_profile_setname(token, "Jack", "N", url)
   
    error = response
    assert error['code'] == 400
    assert error['message'] == '<p>Second name must be between 1 and 50 characters in length</p>'

    requests.delete(url + '/clear')