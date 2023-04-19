import hashlib

# Define the hashed password to be cracked
hashed_password = hashlib.md5("password".encode()).hexdigest()

# Define the password candidate
password_candidate = ""

# Iterate over all possible passwords
iteration_count = 0
while True:
    # Increment the password candidate by one character
    password_candidate += "a"
    
    # Hash the candidate password and compare to the target hash
    hashed_candidate = hashlib.md5(password_candidate.encode()).hexdigest()
    iteration_count += 1
    
    # Print the current iteration count every 1000 iterations
    if iteration_count % 10000 == 0:
        print("Iterations: " + str(iteration_count))
    
    # If the candidate matches the target, print the result and exit the loop
    if hashed_candidate == hashed_password:
        print("Password found: " + password_candidate)
        print("Iterations: " + str(iteration_count))
        break

