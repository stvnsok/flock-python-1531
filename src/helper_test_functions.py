import requests
import json

'''
These are helper functions that will help reduce a lot of boilerplate
in testing. Enjoy :D
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


