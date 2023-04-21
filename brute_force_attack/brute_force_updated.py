#program that brute forces a password
import itertools
import string
import time

#password for testing

test_password = "ba12"

#load the data 

with open("/Users/raresnitu/Documents/security_project/ELEC0138_Project/brute_force_attack/1000-most-common-passwords.txt", "r") as f:
    common_passwords = f.read().splitlines()

with open("/Users/raresnitu/Documents/security_project/ELEC0138_Project/brute_force_attack/dictionary.txt", "r") as f:
    english_dictionary = f.read().splitlines()


#generate a list of possible characters

possible_characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation

#time the program
#start the timer

start_time = time.time()

#test if the password is in the list of common passwords or the dictionary
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
#generate all possible combinations of characters 
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
    


