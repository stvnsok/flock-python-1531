data = {
    'users': [
        {
            'u_id': 1,
            'email': "z55555@ad.unsw.edu.au",
            'password': "password123",
            'name_first': 'Jay',
            'name_last': 'Anand',
            'handle_str': 'JayAnand',
            'token': 1
        },
        {
            'u_id': 2,
            'email': "z3333333@ad.unsw.edu.au",
            'password': "password123",
            'name_first': 'Marko',
            'name_last': 'Wong',
            'handle_str': 'MarkoWong',
            'token': 2
        },
        {
            'u_id': 3,
            'email': "z99999@ad.unsw.edu.au",
            'password': "password123",
            'name_first': 'Bob',
            'name_last': 'Cool',
            'handle_str': 'BobCool',
            'token': 3
        },
    ],
    'messages': [
        {
            'message_id': 1,
            'u_id': 1,
            'message': "yo good m8?",
            'time_created': '10:24'
        },
        {
            'message_id': 2,
            'u_id': 2,
            'message': "Nah I so confused!!",
            'time_created': '10:25'
        },
    ],
    'channels': [
        {
            'id': 1000,
            'name': 'channel1',
            'owner_members': [
                {
                    'u_id': 1,
                    'name_first': 'Jay',
                    'name_last': 'Anand',
                },
                {
                    'u_id': 2,
                    'name_first': 'Marko',
                    'name_last': 'Wong',
                }
            ],
            'all_members': [
                {
                    'u_id': 1,
                    'name_first': 'Jay',
                    'name_last': 'Anand',
                },
                {
                    'u_id': 2,
                    'name_first': 'Marko',
                    'name_last': 'Wong',
                }
            ],
            'messages': []
        },
        {
            'id': 2000,
            'name': 'channel2',
            'owner_members': [
                {
                    'u_id': 1,
                    'name_first': 'Jay',
                    'name_last': 'Anand',
                },
                {
                    'u_id': 2,
                    'name_first': 'Marko',
                    'name_last': 'Wong',
                }
            ],
            'all_members': [
                {
                    'u_id': 1,
                    'name_first': 'Jay',
                    'name_last': 'Anand',
                },
                {
                    'u_id': 2,
                    'name_first': 'Marko',
                    'name_last': 'Wong',
                }
            ],
        },
    ],

}
