Assumptions:
auth_register:
    - the user id is just 1,2,3,.... increasing by 1 per new user
    - the email check can be made using the provided code linked on the specs to 100%
    - comply with the spec reguarding validity of emails
    - When there is an input error, the program should stop

Related to Channels.py
    - channel names can have no characters ''
    - channel names don't need to be unique
    - the key channels in data have an extra is_public value within its' list 
    to identify private or public