#program that brute forces a password

import itertools
import string
import time

#password for testing

test_password = "abcd"

#generate a list of possible characters

possible_characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

#time the program to see how long it takes to crack the password
#start the timer

start_time = time.time()

#generate all possible combinations of characters   

for lenght in range(1, len(test_password)+1):
    for x in itertools.product(possible_characters, repeat= lenght):
        password = "".join(x)
        print("Trying: " + password)
        if password == test_password:
            #stop the timer
            end_time = time.time()
            print("Password cracked: " + password)
            print("Time taken: " + str(end_time - start_time) + " seconds")
            break
    


