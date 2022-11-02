'''

# Concurrency means: I have several things that I want to be tracking at once,
even if they're not necessarily executing at once.

# Parallelism means: I have several things that I want to be tracking at once,
AND they should be executing at once.

In order to have true parallel execution on a computer, then is needed multiple
cores (processors). But there will be more processes running than cores anyway,
which means the computer needs to keep track on the process, swapping it in and
out of memory to the CPUs.

How is possible have multiple things happening in a program, so that we can
break a problem apart and deal with it using concurrency?
    - The oldest, and most traditional way is to use *processes*. The good news
    is that each process runs separately, with its own memory, and is
    independent of other processes. This means that the computer can decide
    which core runs which process and when. The problem is that there's a lot
    of overhead to that -- it takes more memory and switching requires more
    time + resourses.

    - A newer way to do things is threads. If your OS runs multiple processes,
    then your process can contain multiple threads. The ideais that the OS
    tells a process that it now has a chance to run and then inside of that
    process, each thread gets a chance to run. The advantage of threads is
    that they're much lighter weight and thus it's easier to switch between
    them. Plus, because they are in the same process, they can share memory.

Threads weren't ever popular in the UNIX world. But they became super popular
among Windows programmers and in the Java world. The combination forced UNIX
people to admit that maybe threads aren't that bad.

To use threads in python, is needed:
    - The 'threading' module;
    - A function that is wanted to run in a thread (i.e. not serially, but
    in parallel with the "main thread");

'''


# Simple example of threads
# It runs the function serially -- meaning, our python interpreter will
# consist of one process and one thread. It'll run the function 5 times.
def hello():
    print('Hello!')


for i in range(5):
    print(hello())


# Now it runs the function 5 times, but each time it's ran, it's going
# to do so inside of a new thread.
# Meaning: It's not going to run the function ourselves, directly. It's
# going to create a new thread object, and hand it the function is chosen
# to run. The thread object will run the function on our behalf inside of
# a new thread.
import threading  # Needed module


def hello():
    print('Hello!')


# The function "hello" is the argument passed to Thread
t = threading.Thread(target=hello)
t.start()  # Ask t to run the function in a new thread


# It runs the function 5 times, as before, each time in it's own thread
def hello():
    print('Hello!\n', end='')  # Don't add \n to the end of print


for i in range(5):
    t = threading.Thread(target=hello)
    t.start()


# Prove the code above is running concurrently, adding time.sleep to
# the function call in order to see if the function is running in order
# also adding a number to the function call, to identify the threads
import time
import random


def hello(n):
    time.sleep(random.randint(0, 3))  # sleep 0-3 seconds
    print(f'{n} Hello!\n', end='')


for i in range(5):
    # pass i as argument to the function
    t = threading.Thread(target=hello, args=(i,))
    t.start()
