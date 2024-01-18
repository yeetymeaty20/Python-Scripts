# Imports packages
import os
from dotenv import load_dotenv
import dotenv
from cryptography.fernet import Fernet
import base64

def load_env_variables():
    load_dotenv()
    global KEY, PASSWORD_E, PASSWORD_D, KEY_BACKUP
    KEY = os.getenv("KEY")
    PASSWORD_E = os.getenv("PASSWORD")
    PASSWORD_D = base64.b64decode(PASSWORD_E).decode("utf-8", "strict")
    KEY_BACKUP = os.getenv("KEY_BACKUP")

def validate_input(prompt, expected_type, error_message):
    while True:
        user_input = input(prompt)
        try:
            user_input = expected_type(user_input)
            return user_input
        except ValueError:
            print(error_message)


load_env_variables()

# Asks users for their password
def pass_check():

    """
    Asks the user for password and checks if it is correct
    
    Args:
        None
    
    Returns:
        bool: validity of password
    """
    

    user_input = input("Enter password: ")
    if user_input == PASSWORD_D:
        validity = True

        return(validity)
    
    else:
        print("Try again.")
        pass_check()


def welcome():

    """
    Prints out the welcome screen and asks the user for their choice

    Args:
        None

    Returns:
        int: users menu choice

    """
    while True:
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Generate new key")
        print("4. Input key and use to encrypt / decrypt")
        print("5. Print out your current key")
        print("6. Set password (Advanced Users only!!!)")
        print("7. Reset Password and Key")
        print("8. Manage Keys")
        print("9. Encrypt a file")
        print("10. Decrypt a file")

        choice = validate_input("Input a number: ", int, "Please input a number")

        try :
            choice = int(choice)
            return(choice)

        except ValueError:
            print("Please input a number")

    

# Encrypt function
def encrypt_func():

    """
    Encrypts the text the user inputs

    Args:
        None

    Returns:
        str: encrypted text

    """

    text = input("Input text: ")

    try:
        text = str(text)
    
    except ValueError:
        print("Please input text")
        encrypt_func()

    data = bytes(text, encoding="utf-8")
    encryption_tool = Fernet(KEY)
    encrypted = encryption_tool.encrypt(data)

    return(str(encrypted))

# Decrypt function
def decrypt_func():
    """
    Decrypts the text the user inputs

    Args:
        None

    Returns:
        str: decrypted text
    """

    if pass_check() == True:
        data = input("Input encrypted text: ")

        # Remove the "b'" and "'" from the input if they exist
        if data.startswith("b'") and data.endswith("'"):
            data = data[2:-1]

        # Try to decrypt the data
        try:
            encryption_tool = Fernet(KEY)
            decrypted = encryption_tool.decrypt(data.encode())
        except:
            print("Decryption failed.")
            return

        # Try to decode the decrypted data
        try:
            decrypted = decrypted.decode("utf-8", "strict")
        except:
            print("Decoding failed.")
            return

        return decrypted
    else:
        pass_check()


# Key generation
def key_gen():

    """
    Generates a new key and saves it to .env file

    Args:
        None
    
    Returns:
        None
    
    """

    if pass_check() == True:

        key = Fernet.generate_key()
        key_str = key.decode("utf-8", "strict")

        dotenv.set_key(".env", "KEY", key_str)
        
        print("Key generated")

    else:
        pass_check()

# Import custom keys so you can share encrypted messages with others
def custom_key():

    """
    Imports a custom key and saves it to .env file

    Args:
        None

    Returns:
        None
    
    """

    if pass_check() == True:

        key = input("Input key: ")
        key = bytes(key, encoding="utf-8")
        key_str = key.decode("utf-8", "strict")
        dotenv.set_key(".env", "KEY", key_str)        
    else:
        pass_check()

def key_print():

    """
    Prints out the current key

    Args:
        None

    Returns:
        None

    """
    
    if pass_check() == True:
        print(KEY)
    else:
        pass_check()

# Changes password
def set_pass():

    """
    Changes the password

    Args:
        None

    Returns:
        None
    
    """
    
    print("Warning for security reasons this will reset your key as well so you cant access someone elses encryptions by resetting password.")
    key_gen()

    password_d = (input("Input new Password: "))
    double_check = (input("Input new Password again: "))

    if password_d != double_check:
        print("Passwords do not match")
        set_pass()

    password_e = base64.b64encode(bytes(password_d, encoding="utf-8"))
    print("The script will now exit and you password will be affective on next launch")

    dotenv.set_key(".env", "PASSWORD", password_e)
    exit()

    

# Resets the password and generates a new key
def reset():

    """
    Resets the password and generates a new key

    Args:
        None

    Returns:
        None
    
    """

    key_gen()
    default = "Alpine"
    
    dotenv.set_key(".env", "PASSWORD", default)

def managekeys():
    """
    Manages keys

    Args:
        None
    
    Returns:
        None
    """
    while True:
        print("1. Backup a key")
        print("2. Delete backed up key")
        print("3. Restore backed up key as current key")
        print("0. Go back to main menu")
        option_key = validate_input("Input a number: ", int, "Please input a number")

        match option_key:
            case 1:
                if KEY_BACKUP != '':
                    print("Delete this backed up key first")
                backedupkey = input("Input the key: ")
                dotenv.set_key(".env", "KEY_BACKUP", backedupkey)
                break
            case 2:
                ask = input("Are you sure [y/n]]")
                if ask == "y":
                    dotenv.set_key(".env", "KEY_BACKUP", '')
                    break
            case 3:
                ask = input("Are you sure [y/n]")
                if ask == "y":
                    dotenv.set_key(".env", "KEY", KEY_BACKUP)
                    break
            case 0:
                break

def encrypt_file():

    """
    Encrypts a file

    Args:
        None
    
    Returns:
        None
    
    """

    
    cwd_contents = os.listdir(os.curdir)

    for item in cwd_contents:
        print(item)

    filename = input("Input file name: ")
    
    with open(filename, "rb") as file:

        data = file.read()

    encryption_tool = Fernet(KEY)
    encrypted = encryption_tool.encrypt(data)

    with open(filename, "wb") as file:

        file.write(encrypted)
        print("File encrypted")


def decrypt_file():
    
    """
    Decrypts a file

    Args:
        None
    
    Returns:
        None
    
    """

    if pass_check() == True:
        cwd_contents = os.listdir(os.curdir)

        for item in cwd_contents:
            print(item)

        filename = input("Input file name: ")
    
        with open(filename, "rb") as file:

            data = file.read()

        encryption_tool = Fernet(KEY)
        decrypted = encryption_tool.decrypt(data)

        with open(filename, "wb") as file:

            file.write(decrypted)
            print("File decrypted")

    else:
        pass_check()
    
        

# Prompts user if they would like to end the script 
def end():

    """
    Prompts user if they would like to end the script

    Args:
        None
    
    Returns:
        None
    
    """

    while True:
            end = input("End [y/n]")

            try:
                end = str(end)
            except ValueError:
                print("Please input y or n")
                continue

            if end.lower() in ["yes", "y", "no", "n"]:
                if end.lower() in ["yes", "y"]:
                    exit()
                elif end.lower() in ["no", "n"]:
                    return
            else:
                print("Please input y or n")

if KEY == '':
    print("Either this is your first time running the script or YOU changed you key to '',no worries we are generating a new key for you.")
    print("Default password is 'alpine' you should change it after")
    key_gen()

# Controls the users choice throughout the script      
while True:

    load_env_variables()

    choice = welcome()
    
    match choice:                                   # I use match statements because they are easier to read and more efficient than if statements

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
        case 9:
            encrypt_file()
        case 10:
            decrypt_file()

    end()