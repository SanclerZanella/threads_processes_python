'''
Exercise: Hello and goodbye

1. Write two functions, 'hello' and 'goodbye', it will
   take an integer as an ID number, and it'll 'time.sleep'
   for a random number of seconds. (keep small!);

2. Launch 5 threads for each of these functions;

3. You should have a total of 10 lines printed out, 5 from
   'hello' and 5 from 'goodbye'
'''


import threading
import time
import random


def hello(n):
    time.sleep(random.randint(0, 3))  # sleep 0-3 seconds
    print(f'{n} Hello!\n', end='')


def goodbye(n):
    time.sleep(random.randint(0, 3))  # sleep 0-3 seconds
    print(f'{n} Goodbye!\n', end='')


for i in range(5):
    t = threading.Thread(target=hello, args=(i,), name=f'helloThread_{i}')
    t.start()

for i in range(5):
    t = threading.Thread(target=goodbye, args=(i,), name=f'goodbyeThread_{i}')
    t.start()
