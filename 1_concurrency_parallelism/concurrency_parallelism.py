'''

# Concurrency means: I have several things that I want to be tracking at once,
even if they're not necessarily executing at once.

# Parallelism means: I have several things that I want to be tracking at once,
AND they should be executing at once.

In order to have true parallel execution on a computer, then is needed multiple
cores (processors). But there will be more processes running than cores anyway,
which means the computer needs to keep track on the process, swapping it in and
out of memory to the CPUs.

'''
