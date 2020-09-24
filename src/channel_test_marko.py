# Written on 24/09/2020 
# By Marko Wong (z5309371)
# Purpore to test functions in channel.py
import pytest
from channel import *
def test_channel_create():
    assert channel_create("token", "name", "is_public T/F") == 1