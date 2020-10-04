Assumptions:

Related to Channel.py
    - the argument of is_public is an true or false so 1 or 0
    - Within channel_invite if channel don't exist give error: "Channel_id does not exist"
    - Within channel_invite if user don't exit give error: "U_id does not exist"
    - Within channel_invite and channel_details if user is not a member of the channel then give error:
    "Authorised user is not a member of the channel"
    - Within channel_detail if channel don't exist give error: "Channel_id does not exist"
    - Within channel_join give error:"Channel_id refers to a channel that is private"
    if the channel is private
    - Only owners can add or remove other owners
    - messages are under the channels key


Related to auth.py:
    - the user id is just 1,2,3,.... increasing by 1 per new user
    - the email check can be made using the provided code linked on the specs to 100%
    - comply with the spec reguarding validity of emails
    - When there is an input error, the program should stop

Related to Channels.py
    - channel names can have no characters ''
    - channel names don't need to be unique
    - the key channels in data have an extra is_public value within its' list
    to identify private or public
    - within channels there is a key for members
    - Add the creator of the channel as owner when the channel is created
    - Within channel_Create if channel name is too long raise error: "Input Channel Name too long"

General:
    - when token incorrect give error stating: "Token is incorrect/user does not exist"
    - the argument of is_public is an true or false so 1 or 0

    - If a user that is to be added as an owner to a channel that isn't already a member
      is added as a member and made an owner