'''
User.py
16/10/2020
'''
#import urllib.request
import shutil # to save it locally
from PIL import Image
import requests
from flask import request
from error import InputError, AccessError
from other import check
from data import (
                    data,is_valid_token,
                    load_token, get_user)

def is_url_image(image_url):
    '''
    Tests if the image_url was a valid url and if the url is an jpg image
    '''
    image_formats = ("image/jpeg", "image/jpg") # for png images "image/png"
    response = requests.head(image_url)
    img_type = response.headers["content-type"]
    if img_type in image_formats:
        #print(f"image type was {img_type}")
        return True
    return False

def user_profile_photo(token, img_url, x_start, y_start, x_end, y_end):
    '''
    Given a URL of an image on the internet, crops the image within bounds
    (x_start, y_start) and (x_end, y_end). Position (0,0) is the top left.
    '''
    # Check if valid token
    if is_valid_token(token) is not True:
        raise AccessError('Token is incorrect')
    
    # Get the user that is sending the request
    authorised_user = get_user((load_token(token)['u_id']))

    # fetch image via url
    u_id = authorised_user['u_id']
    image_name = f'src/static/user_profile_pic_{u_id}.jpg'

    # Open the url image, and return the stream content.
    response = requests.get(img_url, stream=True)

    # Check if the image was retrieved successfully
    if response.status_code == 200:

        # Allow the image size to be bigger than 0.
        response.raw.decode_content = True

        # Open a local file with wb for the image to be copied into
        with open(image_name, 'wb') as img:
            shutil.copyfileobj(response.raw, img)
        #print('Image sucessfully Downloaded: ', image_name)

    else:
        raise InputError('img_url returned an HTTP status other than 200')
        #print('Image Couldn\'t be retreived')

    #Check if url is an image_url with image type jpg or jpeg
    if is_url_image(img_url) is False:
        raise InputError('Provided url is not a valid jpg image url')

    # crop image
    image_object = Image.open(image_name)
    image_size = image_object.size
    if (
            x_start > image_size[0] or
            int(x_start) < 0 or
            int(x_end) > image_size[0] or
            int(x_end) < 0 or
            int(y_start) > image_size[1] or
            int(y_start) < 0 or
            int(y_end) > image_size[1] or
            int(y_end) < 0
    ):
        raise InputError(
            f"Invalid crop size, the image has dimensions {image_size[0]} x {image_size[1]}"
        )

    #print(image_size)
    cropped = image_object.crop((int(x_start), int(y_start), int(x_end), int(y_end)))
    cropped.save(image_name)

    # input user profile_pic to user database
    curr_url = request.host
    authorised_user['profile_img_url'] = f'http://localhost:{curr_url[10:]}/static/user_profile_pic_{u_id}.jpg'

    return{}



def user_profile(token, u_id):
    '''
    For a valid user, returns information about their user_id, email, first name,
    last name, and handle
    '''
    # Grabs all users from data
    users = data['users']
    
    # Check if valid token
    if is_valid_token(token) is not True:
        raise AccessError('Token is incorrect')
    
    # # Get the user that is sending the request
    # authorised_user = get_user((load_token(token)['u_id']))

    # Searches for the user with the u_id
    users_checked = 0
    for user_id in users:
        if int(user_id['u_id']) == int(u_id):
            profile = user_id
        else:
            users_checked += 1

    # If list reaches end then raise error for no user found
    if users_checked == len(users):
        raise InputError('No users with the entered u_id was found')

    target_user = {
        'u_id': profile['u_id'],
        'email': profile['email'],
        'name_first': profile['name_first'],
        'name_last': profile['name_last'],
        'handle_str': profile['handle_str'],
        'profile_img_url': profile['profile_img_url'],
    }

    return {'user': target_user }
    

def user_profile_sethandle(token, handle_str):
    '''
    Update the authorised user's handle (i.e. display name)
    '''
    # Grabs all users from data
    users = data['users']
    
    # Check if valid token
    if is_valid_token(token) is not True:
        raise AccessError('Token is incorrect')
    
    # Get the user that is sending the request
    authorised_user = get_user((load_token(token)['u_id']))

    # checking if length of handle_str is between 3 and 20 inclusive
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError("Handle length needs to be between 3 and 20")

    # Cycles through all users to check if given handle already exists
    for user_handle in users:
        if user_handle['handle_str'] == handle_str:
            raise InputError('Handle already in use by another user')

    # Update the handle_str of user
    authorised_user['handle_str'] = handle_str

    return {}

def user_profile_setname(token, name_first, name_last):
    '''
    Update the authorised user's first and last name
    '''
    # # Grabs all users from data
    # users = data['users']
    
    # Check if valid token
    if is_valid_token(token) is not True:
        raise AccessError('Token is incorrect')
    
    # Get the user that is sending the request
    authorised_user = get_user((load_token(token)['u_id']))

    # Raise errors for invalid name lengths
    if (len(name_first) > 50) or (len(name_first) < 1):
        raise InputError('First name must be between 1 and 50 characters in length')

    if (len(name_last) > 50) or (len(name_last) < 1):
        raise InputError('Last name must be between 1 and 50 characters in length')
    # Update first name and last name of user
    authorised_user['name_first'] = name_first
    authorised_user['name_last'] = name_last

    return {}

def user_profile_setemail(token, email):
    '''
    Update the authorised user's email address
    '''
    # Grabs all users from data
    users = data['users']

    # Check if valid token
    if is_valid_token(token) is not True:
        raise AccessError('Token is incorrect')
    
    # Get the user that is sending the request
    authorised_user = get_user((load_token(token)['u_id']))

    # Check email is valid format
    if check(email) is not True:
        raise InputError('Email is not valid')

    # Check if the email is already being used by another user
    if any(user['email'] == email and user['u_id'] != authorised_user['u_id'] for user in users):
        raise InputError("Email address is already in use")

    # Set email
    authorised_user['email'] = email
    return {}
