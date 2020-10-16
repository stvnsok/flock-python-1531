'''
Tests for user.py

'''

import user
from error import InputError
from other import clear
from data import data
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
import pytest

# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
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
    resp = requests.get(url + 'user', params={'data': 'hello'})
    assert json.loads(resp.text) == {'data': 'hello'}

def test_profile_invalid_user_unregistered(url):
    pass

def test_profile_U_id_not_found(url):
    pass

def test_profile_display_correct_info(url):
    pass

'''
Tests for user/profile/sethandle
'''
def test_profile_handle_invalid_user_token(url):
    pass

def test_profile_handle_too_short(url):
    pass

def test_profile_handle_too_long(url):
    pass

def test_profile_handle_exisiting():
    pass

def test_profile_handle_correct_update():
    pass


