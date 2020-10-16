# Assumptions

## Related to auth.py
    *   The user id is just 1,2,3,.... increasing by 1 per new user

## Related to channel.py
    *   Only owners can add or remove other owners
    *   Messages are under the channels key

## Related to channels.py
    *   Channel names can have no characters ''
    *   Channel names don't need to be unique
    *   The key channels in data have an extra is_public value within its' list
    to identify private or public
    *   Within channels there is a key for members
    *   Add the creator of the channel as owner when the channel is created
    *   If a user that is to be added as an owner to a channel that isn't already a member is added as a member and made an owner

## Realted to user.py
    * handle_str must be between 3 and 20 characters is INCLUSIVE of 3 and 20
## Related to message.py and messages
    *   Since all messages will have a unique id, they will be stored in their own table rather than be nested within a field of the channel data.

## General:

    