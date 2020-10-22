'''
These are helper functions that will help reduce a lot of boilerplate
in testing. Enjoy :D
'''

import requests


'''
---------------------Auth Functions---------------------
'''


def register_user(email, password, name_first, name_last, url):
    response = requests.post(f'{url}auth/register', json={
        "email": email,
        "password": password,
        "name_first": name_first,
        "name_last": name_last,
    })

    return response.json()


def login_user(email, password, url):
    response = requests.post(f'{url}auth/login', json={
        "email": email,
        "password": password,
    })

    return response.json()


def logout_user(token, url):
    response = requests.post(f'{url}auth/logout', json={
        "token": token
    })

    return response.json()


'''
---------------------Channel Functions---------------------
'''


def channel_invite(token, channel_id, u_id, url):
    response = requests.post(f'{url}channel/invite', json={
        "token": token,
        "channel_id": channel_id,
        "u_id": u_id
    })

    return response.json()


def channel_details(token, channel_id, url):
    response = requests.get(f'{url}channel/details', params={
        "token": token,
        "channel_id": channel_id,
    })

    return response.json()


def channel_messages(token, channel_id, start, url):
    response = requests.get(f'{url}channel/messages', params={
        "token": token,
        "channel_id": channel_id,
    })

    return response.json()


def channel_leave(token, channel_id, url):
    response = requests.post(f'{url}channel/leave', json={
        "token": token,
        "channel_id": channel_id,
    })

    return response.json()


def channel_join(token, channel_id, url):
    response = requests.post(f'{url}channel/join', json={
        "token": token,
        "channel_id": channel_id,
    })

    return response.json()


def channel_addowner(token, channel_id, u_id, url):
    response = requests.post(f'{url}channel/addowner', json={
        "token": token,
        "channel_id": channel_id,
        "u_id": u_id

    })

    return response.json()


def channel_removeowner(token, channel_id, u_id, url):
    response = requests.post(f'{url}channel/removeowner', json={
        "token": token,
        "channel_id": channel_id,
        "u_id": u_id

    })

    return response.json()


'''
---------------------Channels Functions---------------------
'''


def channels_list(token, url):
    response = requests.get(f'{url}channel/list', params={
        "token": token,
    })

    return response.json()


def channels_listall(token, url):
    response = requests.get(f'{url}channel/listall', params={
        "token": token,
    })

    return response.json()


def channels_create(token, name, is_public, url):
    response = requests.post(f'{url}channels/create', json={
        "token": token,
        "name": name,
        "is_public": is_public
    })

    return response.json()


'''
---------------------Message Functions---------------------
'''


def message_send(token, channel_id, message, url):
    response = requests.post(f'{url}message/send', json={
        "token": token,
        "channel_id": channel_id,
        "message": message
    })

    return response.json()


def message_remove(token, message_id, url):
    response = requests.delete(f'{url}message/remove', json={
        "token": token,
        "message_id": message_id,
    })

    return response.json()


def message_edit(token, message_id, message, url):
    response = requests.put(f'{url}message/edit', json={
        "token": token,
        "channel_id": message_id,
        "message": message
    })

    return response.json()


'''
---------------------User Functions---------------------
'''


def user_profile(token, u_id, url):
    response = requests.get(f'{url}user/profile', params={
        "token": token,
        "u_id": u_id,
    })

    return response.json()


def user_profile_setname(token, name_first, name_last, url):
    response = requests.put(f'{url}user/profile/setname', json={
        "token": token,
        "name_first": name_first,
        "name_last": name_last,
    })

    return response.json()


def user_profile_setemail(token, email, url):
    response = requests.put(f'{url}user/profile/setemail', json={
        "token": token,
        "email": email
    })

    return response.json()


def user_profile_sethandle(token, handle_str, url):
    response = requests.put(f'{url}user/profile/sethandle', json={
        "token": token,
        "handle_str": handle_str
    })

    return response.json()


'''
---------------------Other Functions---------------------
'''


def users_all(token, url):
<<<<<<< HEAD
    response = requests.get(f'{url}users/all', params={
        "token": token,
    })
=======
    response = requests.get(f'{url}users/all', params={"token" : token,})
>>>>>>> fixed errors in users_test

    return response.json()


def change_userpermission(token, u_id, permission_id, url):
    response = requests.post(f'{url}admin/userpermission/change', json={
        "token": token,
        "u_id": u_id,
        "permission_id": permission_id
    })

    return response.json()


def search(token, query_str, url):
    response = requests.get(f'{url}search', params={
        "token": token,
        "query_str": query_str
    })

    return response.json()


def clear(url):
    requests.delete(f'{url}clear')
