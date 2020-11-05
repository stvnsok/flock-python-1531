'''
This acts as a 'database'. It will be initialised whenever a test is run (does not persist).

Dictionary layout

This is just to help build iteration 1 features and keep some consistency

User 0bject :  {
                    'u_id' : integer,
                    'email' : string,
                    'password' : string,
                    'name_first' : string,
                    'name_last' : string,
                    'handle_str' : string,
                    'token' : string,
                    'profile_img_url' : string,
                    'permission_id' : integer,
               }

Channel Object : {
                    'channel_id' : integer,
                    'name' : string,
                    'is_public' : boolean,
                    'members' : [
                                    {
                                        'u_id': integer,
                                        'name_first': string,
                                        'name_last': string,
                                        'is_owner': bool
                                    }

                                ],
                    'messages' : [
                                    {
                                        'message_id' : integer,
                                        'u_id' : integer,
                                        'message' : string,
                                        'time_created' : integer (unix timestamp),
                                    }

                                ],
                    'standup': ['marko: here are the instructions',
                                'steven: 'I'm confused',
                                'marko: dw so am I,
                               ],
                    'standup_active': True,
                 }

'''
data = {
    'users': [],
    'channels': [],
}
