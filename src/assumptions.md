Assumptions:
auth_register:
    - the user id is just 1,2,3,.... increasing by 1 per new user
    - the email check can be made using the provided code linked on the specs to 100%
    - comply with the spec reguarding validity of emails
    - When there is an input error, the program should stop

Related to Channels.py
    - channel_id can be any integer, no need rules related to it. Therefore the
    channel_id's will have the following rule the first number will be either 
    1 or 9. If 1 is the first number then it is public else if 9 then private.
    The channel_id in total will have 4 digits with 1st digit as decribed above
    and the rest used to distinish the different channels.

    - As a result of the rule above there can only be 999 channels ever created
    for public and 999 for private.

    - the argument of is_public is an true or false so 1 or 0