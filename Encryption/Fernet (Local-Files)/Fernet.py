# Imports packages
import os
from dotenv import load_dotenv
import dotenv
from cryptography.fernet import Fernet

load_dotenv()

KEY = os.getenv("KEY")
PASSWORD = os.getenv("PASSWORD")
KEY_BACKUP = os.getenv("KEY_BACKUP")


# Asks users for their password
def pass_check():

    user_input = input("Enter password: ")
    if user_input == PASSWORD:
        validity = True

        return(validity)
    
    else:
        print("Try again.")
        pass_check()

# Welcome function
def welcome():

    print("1. Encrypt")
    print("2. Decrypt")
    print("3. Generate new key")
    print("4. Input key and use to encrypt / decrypt")
    print("5. Print out your current key")
    print("6. Set password (Advanced Users only!!!)")
    print("7. Reset Password and Key")
    print("8. Manage Keys")

    choice = int(input("Input number: "))
    return choice

# Encrypt function
def encrypt_func():

    text = str(input("Input text: "))
    data = bytes(text, encoding="utf-8")
    cipher = Fernet(KEY)
    encrypted = cipher.encrypt(data)

    return(str(encrypted))

# Decrypt function
def decrypt_func():

    if pass_check() == True:

        data = str(input("Input encrypted text: "))
    
        cipher = Fernet(KEY)
        decrypted = cipher.decrypt(data)
        return(str(decrypted))
    else:
        pass_check()


# Key generation
def key_gen():

    if pass_check() == True:

        key = Fernet.generate_key()
        key_str = key.decode("utf-8", "strict")

        dotenv.set_key(".env", "KEY", key_str)
    else:
        pass_check()

# Import custom keys so you can share encrypted messages with others
def custom_key():

    if pass_check() == True:

        key = input("Input key: ")
        key = bytes(key, encoding="utf-8")
        key_str = key.decode("utf-8", "strict")
        dotenv.set_key(".env", "KEY", key_str)        
    else:
        pass_check()


    

# Prints out key, you can also read it directly from "thekey.key" file
def key_print():
    
    if pass_check() == True:
        print(KEY)
    else:
        pass_check()

# Changes password
def set_pass():
    
    print("Warning for security reasons this will reset your key as well so you cant access someone elses encryptions by resetting password.")
    key_gen()

    password = (input("Input new Password: "))
    print("The script will now exit and you password will be affective on next launch")

    dotenv.set_key(".env", "PASSWORD", password)
    exit()

    

# Resets the password and generates a new key
def reset():

    key_gen()
    default = "Alpine"
    
    dotenv.set_key(".env", "PASSWORD", default)

def managekeys():

    print("1. Backup a key")
    print("2. Delete backed up key")
    print("3. Restore key from backed up key")
    print("0. Go back to main menu")
    option_key = int(input("Input a number: "))

    match option_key:

        case 1:
            if KEY_BACKUP != '':

                backedupkey = input("Input the key: ")
                dotenv.set_key(".env", "KEY_BACKUP", backedupkey)
            else:
                print("Delete this backed up key first")
                managekeys()
        case 2:
            ask = input("Are you sure [y/n]]")

            if ask == "y":
                dotenv.set_key(".env", "KEY_BACKUP", '')
            else:
                welcome()
        case 3:
            ask = input("Are you sure [y/n]")

            if ask == "y":
                dotenv.set_key(".env", "KEY", KEY_BACKUP)
            else:
                welcome()
        case 0:
            welcome()

# Prompts user if they would like to end the script 
def end():

    end = input("End [y/n]")
    if end == "yes" or end == "y":
        exit()

if KEY == '':
    print("Either this is your first time running the script or YOU changed you key to '',no worries we are generating a new key for you.")
    print("Default password is Alpine you should change it after")
    key_gen()

# Controls the users choice throughout the script      
while True:

    #.env stuff
    load_dotenv()

    KEY = os.getenv("KEY")
    PASSWORD = os.getenv("PASSWORD")
    KEY_BACKUP = os.getenv("KEY_BACKUP")

    choice = welcome()
    
    match choice:

        case 1:
            encrypt = encrypt_func()
            print(encrypt)
        case 2:
            decrypt = decrypt_func()
            print(decrypt)
        case 3:
            key_gen()
        case 4:
            custom_key()
        case 5:
            key_print()
        case 6:
            set_pass()
        case 7:
            reset()
        case 8:
            managekeys()

    end()