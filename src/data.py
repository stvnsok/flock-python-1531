# data = {
#     'users': [
#         #{
#         #    'u_id': 1,
#         #    'email': "z55555@ad.unsw.edu.au",
#         #    'password': "password123",
#         #    'name_first': 'Jay',
#         #    'name_last': 'Anand',
#         #    'handle_str': 'JayAnand',
#         #},
#         #{
#         #    'u_id': 2,
#         #    'email': "z3333333@ad.unsw.edu.au",
#         #    'password': "password123",
#         #    'name_first': 'Marko',
#         #    'name_last': 'Wong',
#         #    'handle_str': 'MarkoWong',
#         #},
#     ],
#     'messages': ['''
#         {
#             'message_id': 1,
#             'u_id': 1 <- Means it from jay
#             'message': "yo good m8?"
#             'time_created': '10:24'
#         },
#         {
#             'message_id': 2,
#             'u_id': 2 <- Means it from Marko
#             'message': "Nah I so confused!!"
#             'time_created': '10:25'
#         },'''
#     ],
#     'channels': ['''
#         {
#             'id': 1000,
#             'name' : 'channel1',
#         },
#         {
#             'id': 2000,
#             'name' : 'channel2',
#         },'''
#     ],
#     'members': ['''
#         {
#             'u_id': 1
#             'name_first': 'jay'
#             'name_last': 'Anand'
#         }
#         {
#             'u_id': 2
#             'name_first': 'Marko'
#             'name_last': 'Wong'
#         }'''
#     ],
# }

'''
This acts as a 'pretend' database. It will be initialised whenever a test is run (does not persist)
'''
data = {
    'users': [],
    'channels': [],
    'messages': [],
    'members': []
}
