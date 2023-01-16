'''

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


'''
THINGS TO KNOW:
    1.Threads can be named, which makes easier to identify
      just pass "name=" when we create a new thread object;

    2. We can always get the currently running thread object
       from 'threading.current_thread()', then getting the
       name og the current thread with
       'threading.current_thread().name';

    3. Because we're not running our function directly, but
       rather outsourcing it to the threading system, our
       function will not return to us. Any return value will
       ignored;
'''


'''

When do threads give up the CPU?

    1. When 5ms (about) pass. Python will allow a thread to run as many
       bytecodes as it wants within that time slice. But as soon as the time
       is up, the current thread can finish the current bytecode, and then it
       gives up the CPU;

    2. Every time a thread handles I/O (input/output), it gives us control of
       the CPU to another thread. That's because I/O (disk/network/screen)
       takes so long compared with everything else, it's not worth keeping
       the CPU when we'll be waiting.

    When we say 'print('a')' in python, we're basically saying: (1) Print the
    string 'a', then (2) print '\n' (new line). because these are two separate
    outputs to I/O, the threads often (not always, but often) gives up control.

'''


import dis  # Disassembly module in python


dis.dis(hello)  # Show the bytecodes for the "hello" function


# Print something when it's done
import threading
import time
import random


def hello(n):
    time.sleep(random.randint(0, 3))  # sleep 0-3 seconds
    print(f'{n} Hello!\n', end='')


for i in range(5):
    # pass i as argument to the function
    t = threading.Thread(target=hello, args=(i,))
    t.start()

print('*** DONE! ***')  # This print will be outputed first


'''

What to do in order to wait all the threads to complete then print a DONE
message?

Use "join".
"join" is a method we can run on a thread object. It means "I'll wait for
you to finish"

'''


import threading
import time
import random


def hello(n):
    time.sleep(random.randint(0, 3))  # sleep 0-3 seconds
    print(f'{n} Hello!\n', end='')


for i in range(5):
    # pass i as argument to the function
    t = threading.Thread(target=hello, args=(i,))
    t.start()
    t.join()  # Wait for this thread run, and then go create a new one.

print('*** DONE! ***')  # This print will be outputed first


# Put all threads in a list then iterate over that list, joining each thread.
# When it's done joining each thread, it's known that threy're all done.

def hello(n):
    time.sleep(random.randint(0, 3))  # sleep 0-3 seconds
    print(f'{n} Hello!\n', end='')


all_threads = list()
for i in range(5):
    t = threading.Thread(target=hello, args=(i,))
    t.start()
    all_threads.append(t)

# Now go through each thread, and join it (i.e. wait for it)
for one_thread in all_threads:
    # Join blocks, it hangs, waiting for the thread to finish
    one_thread.join()

# By the time this line is reached and guaranteed that all of the threads
# are done.
print('*** DONE! ***')


# Another way is to invoke join with an argument, a float that tells the join
# how long it's willing to wait if that much time passes without the thread
# ending, it'll be able to go onto another thread.

# As we create each thread (and launch our function in it), we store our
# thread in all_threads. Then, after our threads have launched, we
# repeatedly iterate through all_threads. With each iteration over
# all_threads, we give one_thread the chance to say "Yes, I'm done!".
# We do that with "join" (one_thread.join()). But we don't want to give
# the thread forever to tell us it's done, so we give it 0.1 seconds
# to tell us that. If the thread is done, then we remove it from all_threads.
# If the thread is NOT done, we go onto the next one. When all_threads is
# empty, we stop iterating over it.

import threading
import time
import random


# Define function
def hello(n):
    time.sleep(random.randint(0, 3))
    print(f'{n} Hello!\n', end='')


#  Launch thread
all_threads = list()
for i in range(5):
    t = threading.Thread(target=hello, args=(i,))
    t.start()
    all_threads.append(t)

# Go through all_threads as many times as we need, giving each thread
# a chance to be joined. When it's joined, we remove the thread from
# the all_threads list

# Wait for each thread to finish
while all_threads:
    for one_thread in all_threads:
        one_thread.join(0.1)  # Wait up to 0.1 seconds for the thread to end

        if not one_thread.is_alive():  # if the thread died, then let's remove it from the list
            print(f'\tRemoved {one_thread.name}')
            all_threads.remove(one_thread)

# By the time this line is reached and guaranteed that all of the threads
# are done
print('*** DONE! ***')
