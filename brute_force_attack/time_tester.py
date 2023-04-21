import string


# password for testing
test_password = input("Which password do you want to test?: ") 

# generate a list of possible characters
characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
num_characters = len(characters)

# set the hashes per second to a conservative estimate
hashes_per_second = 1000000

# loop over different password lengths
for length in range(1, len(test_password) + 1):
    print("Testing password length:", length)

    # estimate the time it would take to generate all possible passwords of this length
    num_possible_passwords = num_characters ** length
    seconds = num_possible_passwords / hashes_per_second

    # convert the time
    years = int(seconds / (60 * 60 * 24 * 365))
    days = int((seconds / (60 * 60 * 24)) % 365)
    hours = int((seconds / (60 * 60)) % 24)
    minutes = int((seconds / 60) % 60)
    

    # print the estimated time
    print("Estimated time to generate all possible passwords of length", length, ":")
    print(years, "years,", days, "days,", hours, "hours,", minutes, "minutes,", seconds, "seconds")
