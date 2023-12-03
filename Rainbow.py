
#!/usr/bin/env python
import hashlib

def hashFunction(text):     #Function to hash password using MD5
    return hashlib.md5(text.encode()).hexdigest()

def reductionFunction(hash_value, password_list): #Function to reduce hash and map it to a password
    hash_as_number = int(hash_value, 16)
    index = hash_as_number % len(password_list)
    return password_list[index]

def generate_rainbow_table(passwords):
    rainbow_table = {}
    used_words = set()

    for word in passwords:
        list = []
        if word not in used_words:
            used_words.add(word)
            list.append(word)
            current_hash = hashFunction(word)

            for i in range(6):  # 7 passwords in a record
                nextPassword = reductionFunction(current_hash,passwords)
                #if nextPassword in used_words:
                    #break
                used_words.add(nextPassword)
                list.append(nextPassword)
                current_hash = hashFunction(nextPassword)
            #print(list)        In case you want to view the whole linked list (contains duplications as i did not handle collision)

            rainbow_table[word] = current_hash  #Store the original word and final current hash in the rainbow table

    sorted_rainbow_table = {k: v for k, v in sorted(rainbow_table.items(), key=lambda item: item[1])}     #Sort the rainbow tables with the key : value pairs

    return sorted_rainbow_table

def save_rainbow_table_to_file(file_name, rainbow_table):       #Function to write rainbow table to new text file
    with open(file_name, 'w') as file:
        for password, hash_value in rainbow_table.items():
            file.write(f"{password} {hash_value}\n")

def is_hash_in_rainbow_table(user_input, rainbow_table):
    for rainbow_hash in rainbow_table.values():
        if user_input == rainbow_hash:
            return True
    return False

def find_preimage(hash_value, rainbow_table):
    preimages = []

    for password, rainbow_hash in rainbow_table.items():
        if hash_value == rainbow_hash:
            preimages.append(password)
        else:
            temp_hash = hash_value
            for _ in range(6):          #Reduction for length of rainbow table record
                temp_hash = hashFunction(reductionFunction(temp_hash, passwords))
                if temp_hash == rainbow_hash:
                    preimages.append(password)
                    break

    return preimages

def find_password(preimage, user_input, passwords):     #Function to check the hash of every password in the link list against user_input
    for preimage in preimages:
        current_hash = hashFunction(preimage)
        if current_hash == user_input:
            return preimage                     #If the first password in link list hashed == user_input, return the password
        else:
            for _ in range(6):                  #Else check every hash for subsequent password
                reduced_word = reductionFunction(current_hash, passwords)
                current_hash = hashFunction(reduced_word)
                if current_hash == user_input:
                    return reduced_word         #Return password

    print("Password not found")

if __name__ == "__main__":

    password_file = "Passwords.txt"  # Replace with your password file
    with open(password_file, "r") as file:
        passwords = [line.strip() for line in file]

    print("Number of passwords read in: " + str(len(passwords)))

    rainbow_table = generate_rainbow_table(passwords)
    print(f"Number of lines in the rainbow table: {len(rainbow_table)}")
    print("")
    save_rainbow_table_to_file("Rainbow.txt", rainbow_table)


    user_input = input("Enter a hash value to find its pre-image: ")
    print("")

    if len(user_input) != 32:
        print("Invalid hash value length. It should be 32 characters.")
    else:
        if is_hash_in_rainbow_table(user_input, rainbow_table):
            print("Hash value found in rainbow table")
            print("Computing to find password")
        else:
            print("Hash value not found in rainbow table at first glance")
            print("Computing hashing and reducing to find if hash value exist in rainbow table")

        print("")
        preimages = find_preimage(user_input, rainbow_table) #many preimages because depends on the position of the password, and number of reduction, might exceed record
        #print(preimages)
        result = find_password(preimages, user_input, passwords)
        if result is not None:
            print("The password is: " + result)

