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

# Encrypt function
def encrypt_func():
    text = str(input("Input text: "))
    data = bytes(text, encoding="utf-8")
    
    

# Decrypt function
def decrypt_func():
    
    User_Input = input("Input your password: ")
    
    mycursor.execute("SELECT data FROM fernet_data WHERE id = 1;")
    result = mycursor.fetchall()
    
    print(result)
    for password in result:
        print(password)
    
    if User_Input == result:
        print("Correct")

    else:
        print("Try again")

    
    

# Key generation
def key_gen():

    key = Fernet.generate_key()
    
    with open("thekey.key", "wb") as thekey:
        thekey.write(key)
        
        print("Key: ", key)
        print("Dont worry this isnt your actual key this is just to make sure its genrating the key correcly")
        print("New key generated you can check your key from the welcome menu")

    key = Fernet.generate_key()
    cipher = Fernet(key)
    with open("thekey.key", "wb") as thekey:
        thekey.write(key)
    
    return cipher 

# Import custom keys so you can share encrypted messages with others
def custom_key():

    key = input("Input key: ")
    key = bytes(key, encoding="utf-8")

    with open("thekey.key", "wb") as thekey:
        thekey.write(key)

    cipher = Fernet(key)
    return cipher

# Prints out key, you can also read it directly from "thekey.key" file
def key_print():
    with open("password.pass", "r") as thepass:
       correct_password = thepass.read()
    password = (input("Enter Password: "))
    

    if password == correct_password:
        if os.path.exists("thekey.key"):
            with open("thekey.key", "rb") as thekey:
                key = thekey.read()
                print("Key: ", key)
    else:
        print("Incorrect Password, try again")
        key_print()

# Changes password
def set_pass():
    
    print("Warning for security reasons this will reset your key as well so you cant access someone elses encryptions by resetting password.")
    key_gen()

    password = (input("Input new Password: "))
    pass_bytes = bytes(password, encoding="utf-8")

    if os.path.exists("password.pass"):
        with open("password.pass", "wb") as thepass:
            thepass.write(pass_bytes)

# Resets the password and generates a new key
def reset():
    default = "Alpine"
    data = bytes(default, encoding="utf-8")
    
    if os.path.exists("password.pass"):
        with open("password.pass", "wb") as thepass:
            thepass.write(data)

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