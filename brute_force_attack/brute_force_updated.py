#program that brute forces a password

import itertools
import string
import time

#password for testing

test_password = "password"

#load the data from 1000-most-common-passwords.txt and dictionary.txt into a list

with open("1000-most-common-passwords.txt", "r") as f:
    common_passwords = f.read().splitlines()

with open("dictionary.txt", "r") as f:
    english_dictionary = f.read().splitlines()


#generate a list of possible characters

possible_characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

#time the program to see how long it takes to crack the password
#start the timer

start_time = time.time()

#generate all possible combinations of characters   
if test_password in common_passwords:
    password = test_password
    end_time = time.time()
    print("Password cracked: " + password)
    print("Time taken: " + str(end_time - start_time) + " seconds")
    print("Password found in common passwords")
elif test_password in english_dictionary:
    password = test_password
    end_time = time.time()
    print("Password cracked: " + password)
    print("Time taken: " + str(end_time - start_time) + " seconds")
    print("Password found in dictionary")

else:
    print("Password not found in common passwords or dictionary")
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
    


