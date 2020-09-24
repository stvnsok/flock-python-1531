Assumptions:

Related to Channel.py
    - channel_id can be any integer, no need rules related to it. Therefore the
    channel_id's will have the following rule the first number will be either 
    1 or 9. If 1 is the first number then it is public else if 9 then private.
    The channel_id in total will have 4 digits with 1st digit as decribed above
    and the rest used to distinish the different channels.

    - As a result of the rule above there can only be 999 channels ever created
    for public and 999 for private.

    - the argument of is_public is an true or false so 1 or 0