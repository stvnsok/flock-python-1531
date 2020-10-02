# Written on 24/09/2020
# Purpose to test functions in channel.py
import pytest
import channel
import channels
import auth
from error import InputError, AccessError
from other import clear

def test_channel_1():
    john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
    bob = auth.auth_register('bob@gmail.com', 'abc123!@#', 'Bob', 'Lime')
    cool_channel = channels.channels_create(john['token'], 'cool_channel', True)

    ch_details = channel.channel_details(john['token'], cool_channel['channel_id'])
    assert ch_details['name'] == 'cool_channel'
    assert len(ch_details['owner_members']) == len(ch_details['all_members']) == 1

    with pytest.raises(InputError) as e:
        channel.channel_invite(john['token'], 9999, bob['u_id'])
    assert str(e.value) == 'Channel_id does not exist'

    with pytest.raises(InputError) as e:
        channel.channel_invite(john['token'], cool_channel['channel_id'], 9999)
    assert str(e.value) == 'U_id does not exist'

    with pytest.raises(AccessError) as e:
        channel.channel_invite(bob['token'], cool_channel['channel_id'], john['u_id'])
    assert str(e.value) == 'Authorised user is not a member of the channel'

    channel.channel_invite(john['token'], cool_channel['channel_id'], bob['u_id'])
    ch_details = channel.channel_details(john['token'], cool_channel['channel_id'])

    assert ch_details['name'] == 'cool_channel'
    assert len(ch_details['owner_members']) == 1
    assert len(ch_details['all_members']) == 2
    
    channel.channel_leave(bob['token'], cool_channel['channel_id'])
    ch_details = channel.channel_details(john['token'], cool_channel['channel_id'])
    assert len(ch_details['owner_members']) == len(ch_details['all_members']) == 1

    channel.channel_addowner(john['token'], cool_channel['channel_id'], bob['u_id'])
    ch_details = channel.channel_details(john['token'], cool_channel['channel_id'])
    assert len(ch_details['owner_members']) == len(ch_details['all_members']) == 2

    channel.channel_removeowner(john['token'], cool_channel['channel_id'], bob['u_id'])
    ch_details = channel.channel_details(john['token'], cool_channel['channel_id'])
    assert len(ch_details['owner_members']) == 1
    assert len(ch_details['all_members']) == 2

    clear()

# def test_channel_details():
#     john = auth.auth_register('john@gmail.com', 'qwe123!@#', 'John', 'Smith')
#     cool_channel = channels.channels_create(john['token'], 'cool_channel', True)
    
#     ch_details = channel.channel_details(john['token'], cool_channel['channel_id'])
#     assert len(ch_details['owner_members']) == len(ch_details['all_members']) == 1

#     clear()


# def test_invite_to_invalid_channel():
#     channels.channels_create(login['token'], "channel_1", True)

# Test that channel invite works correctly


# def test_channel_invite():
#     clear()
#     result = channel.channel_invite(1, 1000, 3)
#     assert result == {}

# # Test invalid channel exception


# def test_channel_invite_invalid_channel():
#     clear()
#     with pytest.raises(InputError) as e:
#         channel.channel_invite(1, 99, 3)
#     assert 'Channel_id does not exist' == str(e.value)

# # Test invalid u_id exception


# def test_channel_invite_invalid_user():
#     clear()
#     with pytest.raises(InputError) as e:
#         channel.channel_invite(1, 1000, 30)
#     assert 'U_id does not exist' == str(e.value)

# # Test unauthorised user exception


# def test_channel_invite_unauthorised_user():
#     clear()
#     with pytest.raises(AccessError) as e:
#         channel.channel_invite(3, 1000, 1)
#     assert 'Authorised user is not a member of the channel' == str(e.value)

# # Test channel details


# def test_channel_details():
#     clear()

#     result = channel.channel_details(1, 2000)
#     assert result == {
#         'name': 'channel2',
#         'owner_members': [
#                 {
#                     'u_id': 1,
#                     'name_first': 'Jay',
#                     'name_last': 'Anand',
#                 },
#             {
#                     'u_id': 2,
#                     'name_first': 'Marko',
#                     'name_last': 'Wong',
#             }
#         ],
#         'all_members': [
#             {
#                 'u_id': 1,
#                 'name_first': 'Jay',
#                 'name_last': 'Anand',
#             },
#             {
#                 'u_id': 2,
#                 'name_first': 'Marko',
#                 'name_last': 'Wong',
#             }
#         ],
#     }

#     result = channel.channel_details(1, 1000)
#     channel.channel_invite(1, 1000, 3)
#     assert result == {
#         'name': 'channel1',
#         'owner_members': [
#                 {
#                     'u_id': 1,
#                     'name_first': 'Jay',
#                     'name_last': 'Anand',
#                 },
#             {
#                     'u_id': 2,
#                     'name_first': 'Marko',
#                     'name_last': 'Wong',
#             },

#         ],
#         'all_members': [
#             {
#                 'u_id': 1,
#                 'name_first': 'Jay',
#                 'name_last': 'Anand',
#             },
#             {
#                 'u_id': 2,
#                 'name_first': 'Marko',
#                 'name_last': 'Wong',
#             },
#             {
#                 'u_id': 3,
#                 'name_first': 'Bob',
#                 'name_last': 'Cool',
#             }
#         ],
#     }


# # Test an invalid channel id
# def test_channel_details_invalid_channel():
#     clear()
#     with pytest.raises(InputError) as e:
#         channel.channel_details(1, 900000)
#     assert 'Channel_id does not exist' == str(e.value)

# # Test an unauthorised member


# def test_channel_details_unauthorised_user():
#     clear()
#     with pytest.raises(AccessError) as e:
#         channel.channel_details(3, 1000)
#     assert 'Authorised user is not a member of the channel' == str(e.value)

