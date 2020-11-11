# Assumptions

## Related to auth.py
    *   The user id is just 1,2,3,.... increasing by 1 per new user

## Related to channel.py
    *   Only owners can add or remove other owners
    *   Messages are under the channels key
    *   The order of the members in the dictionary are in the order the members 
    were invited.

## Related to channels.py
    *   Channel names can have no characters ''
    *   Channel names don't need to be unique
    *   The key channels in data have an extra is_public value within its' list
    to identify private or public
    *   Within channels there is a key for members
    *   Add the creator of the channel as owner when the channel is created
    *   If a user that is to be added as an owner to a channel that isn't already a member is added as a member and made an owner

## Related to user.py
    *   handle_str must be between 3 and 20 characters is INCLUSIVE of 3 and 20
    *   profile_img_url will be empty until the user uploads a photo
    *   The profile pics stored in the static folder will never be deleted but will be
    overwitten, as the naming convention allows only have one pic per user.

## Related to standup.py
    *   The standup functions can be used by authorised users that is not part of the channel.
    *   Assuming standup/send will replace any message_send during active standup

## Related to message.py and messages
    *   For message/edit an empty string is a string that has no white space at all, therefore will have a length of zero without performing any stripping

    *   Message objects only require time created, therefore when a message is edited, it will not create a new message object, but simply update the message field of the existing message object

## Related to permissions
    *   Channel permissions will be separate to global permissions. Global permissions are admin rights across the Flockr app, whereas a channel permissions are limited to the scope of the selected channel. Channel permissions will work how regular admin permissions work in other messaging apps. 
    *   Permission_id will be stored in both the user object and channel.members object. Only the first user to sign up to Flock is a a global admin. Anyone that creates a channel is admin of that channel, not of Flockr.

    *   Since we used a boolean 'is_owner' to determine whether a member is the creator or owner of a channel, we will continue to use that as it is embedded in iteration1 tests. Spec only requires a permission id be set as a global variable.

## General:
    * if token is invalid there should not be any other error messages before it

    