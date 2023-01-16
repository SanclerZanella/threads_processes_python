'''
Exercise: Vowel Counts

1. Write a function that takes a filename (a string) as an argument. In the
   function, it'll create a dictionary for each of the vowels in english
   (a, e, i, o and u), with a value of 0. The function should then iterate
   over every character in the file, and count how many of each vowel there is;

2. Get five filenames for text files on your system, and put them in a list;

3. Launch a new thread for each of the files in the list of filenames;

4. Join the threads together and indicate the threads are done.
'''

import threading
import os


def vowel_counts(filename):
    vowels = dict.fromkeys('aeiou', 0)

    for char in filename:
        if char in vowels.keys():
            vowels[char] += 1

    print(f'{filename}: {vowels}')


# files = os.listdir("../mock_files")[0:5]

# # Launching threads for the files
# all_threads = list()
# for filename in files:
#     t = threading.Thread(target=vowel_counts, args=(filename,),
#                          name=f'vowel_counts-{filename}')
#     t.start()
#     all_threads.append(t)

# # Join the threads -- meaning, wait them to finish
# while all_threads:
#     for one_thread in all_threads:
#         one_thread.join(0.01)

#         if not one_thread.is_alive():
#             print(f'\tRemoved {one_thread.name}')
#             all_threads.remove(one_thread)

# print("*** DONE! ***")


# vvv Another way to iterate over the threads vvv

files = os.listdir("../mock_files")[0:5]

pre_run_thread_count = threading.active_count()

# Launching threads for the files
for filename in files:
    t = threading.Thread(target=vowel_counts, args=(filename,),
                         name=f'vowel_counts-{filename}')
    t.start()

# Join the threads -- meaning, wait them to finish
# So long as we have more than just the main thread
while threading.active_count() > pre_run_thread_count:
    for one_thread in threading.enumerate():

        # You cannot join the main thread to itself
        if one_thread == threading.current_thread():
            continue

        one_thread.join(0.01)

print("*** DONE! ***")
