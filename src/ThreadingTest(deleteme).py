# import threading
# import time
 
# def hello(string):
#     print('hello')
#     print(f"hello, Timer: {string}")
#     #print(f"type was: {type(arg)}")
#     # do something

# def hello(string):
#     print(string)


# if __name__ == '__main__':
#     string = 'yo'
#     #t = threading.Timer(3.0, hello, ["yes sisr"])
#     t = threading.Timer(2, hello, args=(string,))
#     t.start()
    
#     print("Starting")

import threading
import time
def hello(string, string2):
    answer = '\n'.join(string)
    print(f'hello there {answer} {string2}')

if __name__ == '__main__':
    string = ['marko', 'wong', 'desu']
    string2 = 'ok'
    t = threading.Timer(2, hello, [string, string2])
    t.start()
    print('starting')