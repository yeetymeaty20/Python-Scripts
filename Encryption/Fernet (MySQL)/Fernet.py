# Imports packages
import os
import mysql.connector
from cryptography.fernet import Fernet

MySQL_password = input("Please input your MySQL 'root' password: ")

fernet_data = mysql.connector.connect (
    host = "localhost",
    user = "root",
    password = MySQL_password,
    database = "fernet"
)

mycursor = fernet_data.cursor()

# Welcome function
def welcome():

    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Generate new key")
    print("4. Input key and use to encrypt / decrypt")
    print("5. Print out your current key")
    print("6. Set password (Advanced Users only!!!)")
    print("7. Reset Password and Key")

    choice = int(input("Input number: "))
    return choice

def pass_check():
    
    User_Input = input("Input your password: ")
    
    mycursor.execute("SELECT data FROM fernet_data WHERE id = 1;")
    result = mycursor.fetchone()
    password = str(result[0])

    print(password)
    
    
    if User_Input == password:
        print("Correct")
        vaild = True

    else:
        print("Try again")
        pass_check()

    return vaild


# Encrypt function
def encrypt_func():

    text = str(input("Input text: "))
    data = bytes(text, encoding="utf-8")
    
    mycursor.execute("SELECT data FROM fernet_data WHERE id = 2;")
    result = mycursor.fetchone()
    key = str(result[0])    
    cipher = Fernet(key)

    encrypted = cipher.encrypt(data)

    return encrypted

# Decrypt function
def decrypt_func():
    
    if pass_check() == True:

        encrypted = str(input("Input encrypted text: "))

        mycursor.execute("SELECT data FROM fernet_data WHERE id = 2;")
        result = mycursor.fetchone()
        key = str(result[0])    
        cipher = Fernet(key)

        decrypted = cipher.decrypt(encrypted)

        return decrypted

# Key generation
def key_gen():
    
    key = Fernet.generate_key()
    key_str = str(key, 'utf-8')
    
    change = "UPDATE fernet_data SET data = '%s' WHERE id = 2;" % (key_str)

    mycursor.execute(change)

    fernet_data.commit()

# Import custom keys so you can share encrypted messages with others
def custom_key():

    key = input("Input key: ")

    imported_key = "UPDATE fernet_data SET data = '%s' WHERE id = 2;" % (key)

    mycursor.execute(imported_key)

    fernet_data.commit()
    
# Prints out the key
def key_print():
    
    mycursor.execute("SELECT data FROM fernet_data WHERE id = 2;")
    result = mycursor.fetchone()
    key = str(result[0])

    print(key)
    

# Changes password
def set_pass():
    
    pass_check()
    new_pass = input("Please Input new password: ")

    change_pass = "UPDATE fernet_data SET data = '%s' WHERE id = 1;" % (new_pass)

    mycursor.execute(change_pass)

    fernet_data.commit()

    
# Resets the password and generates a new key
def reset():
    default = "Alpine"
    
    change_pass = "UPDATE fernet_data SET data = '%s' WHERE id = 1;" % (default)

    mycursor.execute(change_pass)

    fernet_data.commit()

    key_gen()

# Prompts user if they would like to end the script 
def end():

    end = input("End [y/n]")
    if end == "yes" or end == "y":
        exit()

# Controls the users choice throughout the script      
while True:

    choice = welcome()
    
    if choice == 1:
        encrypt = encrypt_func()
        print(encrypt)
        end()
        
    elif choice == 2:
        decrypt = decrypt_func()
        print(decrypt)
        end()
        
    elif choice == 3:
        key_gen()
        end()
        
    elif choice == 4:
        custom_key()
        end()
        
    elif choice == 5:
        key_print()
        end()

    elif choice == 6:
        set_pass()
        end()

    elif choice == 7:
        reset()
        end()