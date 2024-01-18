# Imports packages
import os
from dotenv import load_dotenv
import dotenv
from cryptography.fernet import Fernet
import base64
import colorama

GREEN = colorama.Fore.GREEN
RED = colorama.Fore.RED
CYAN = colorama.Fore.CYAN
YELLOW = colorama.Fore.YELLOW
MAGENTA = colorama.Fore.MAGENTA

L_GREEN = colorama.Fore.LIGHTGREEN_EX
L_RED = colorama.Fore.LIGHTRED_EX
L_CYAN = colorama.Fore.LIGHTCYAN_EX
L_YELLOW = colorama.Fore.LIGHTYELLOW_EX
L_MAGENTA = colorama.Fore.LIGHTMAGENTA_EX

RESET = colorama.Fore.RESET

def load_env_variables():
    
    os.environ.clear()
    load_dotenv(dotenv_path=".env")
    KEY = os.getenv("KEY")
    PASSWORD_E = os.getenv("PASSWORD")
    PASSWORD_D = base64.b64decode(PASSWORD_E).decode("utf-8", "strict")
    KEY_BACKUP = os.getenv("KEY_BACKUP")

    DEBUG = os.getenv("DEBUG")

    return KEY, PASSWORD_E, PASSWORD_D, KEY_BACKUP, DEBUG

def validate_input(prompt, expected_type, error_message):
    while True:
        user_input = input(L_YELLOW + prompt + RESET)
        try:
            user_input = expected_type(user_input)
            return user_input
        except ValueError:
            print(L_RED + error_message + RESET)


load_env_variables()

# Asks users for their password
def pass_check(PASSWORD_D):

    """
    Asks the user for password and checks if it is correct
    
    Args:
        None
    
    Returns:
        bool: validity of password
    """
    
    while True:
        user_input = input(L_YELLOW + "Enter password: " + RESET)
        if user_input == PASSWORD_D:
            return True
        else:
            print(L_RED + "Try again." + RESET)

def main():
    """
    Prints out the welcome screen and asks the user for their choice

    Args:
        None

    Returns:
        int: users menu choice
    """
    menu_options = [
        L_CYAN + "1. Encrypt",
        L_CYAN + "2. Decrypt",
        L_CYAN + "3. Generate new key",
        L_CYAN + "4. Input key and use to encrypt / decrypt",
        L_CYAN + "5. Print out your current key",
        L_CYAN + "6. Set password",
        L_CYAN + "7. Reset Password and Key",
        L_CYAN + "8. Manage Keys",
        L_CYAN + "9. Encrypt a file",
        L_CYAN + "10. Decrypt a file",
        L_CYAN + "0. Debug mode" + RESET
    ]

    print("\n".join(menu_options))

    choice = validate_input("Input a number: ", int, "Please input a number")

    try:
        choice = int(choice)
        return choice
    except ValueError:
        print(L_RED + "Please input a number" + RESET)

    

# Encrypt function
def encrypt_func(KEY):

    """
    Encrypts the text the user inputs

    Args:
        None

    Returns:
        str: encrypted text

    """

    text = validate_input("Input text: ", str, "Please input text")

    data = bytes(text, encoding="utf-8")
    encryption_tool = Fernet(KEY)
    encrypted = encryption_tool.encrypt(data)

    return(str(encrypted))

# Decrypt function
def decrypt_func(KEY, PASSWORD_D):
    """
    Decrypts the text the user inputs

    Args:
        None

    Returns:
        str: decrypted text
    """

    if pass_check(PASSWORD_D) == True:

        data = validate_input("Input text: ", str, "Please input text")

        # Remove the "b'" and "'" from the input if they exist
        if data.startswith("b'") and data.endswith("'"):
            data = data[2:-1]

        # Try to decrypt the data
        try:
            encryption_tool = Fernet(KEY)
            decrypted = encryption_tool.decrypt(data.encode())
        except:
            print(L_RED + "Decryption failed." + RESET)
            return

        # Try to decode the decrypted data
        try:
            decrypted = decrypted.decode("utf-8", "strict")
        except:
            print(L_RED + "Decoding failed." + RESET)
            return

        return decrypted
    else:
        pass_check(PASSWORD_D)


# Key generation
def key_gen(PASSWORD_D):

    """
    Generates a new key and saves it to .env file

    Args:
        None
    
    Returns:
        None
    
    """

    if pass_check(PASSWORD_D) == True:

        key = Fernet.generate_key()
        key_str = key.decode("utf-8", "strict")

        dotenv.set_key(".env", "KEY", key_str)

        load_env_variables
        print("Key generated")

    else:
        pass_check(PASSWORD_D)

# Import custom keys so you can share encrypted messages with others
def custom_key(PASSWORD_D):

    """
    Imports a custom key and saves it to .env file

    Args:
        None

    Returns:
        None
    
    """

    if pass_check(PASSWORD_D) == True:

        key = input("Input key: ")
        key = bytes(key, encoding="utf-8")
        key_str = key.decode("utf-8", "strict")
        dotenv.set_key(".env", "KEY", key_str)

        load_env_variables()     
    else:
        pass_check(PASSWORD_D)

def key_print(KEY, PASSWORD_D):

    """
    Prints out the current key

    Args:
        None

    Returns:
        None

    """
    
    if pass_check(PASSWORD_D) == True:
        print(KEY)
    else:
        pass_check(PASSWORD_D)

# Changes password
def set_pass(PASSWORD_D):

    """
    Changes the password

    Args:
        None

    Returns:
        None
    
    """
    
    print("Warning for security reasons this will reset your key as well so you cant access someone elses encryptions by resetting password.")
    key_gen(PASSWORD_D)

    password_d = (input("Input new Password: "))
    double_check = (input("Input new Password again: "))

    if password_d != double_check:
        print("Passwords do not match")
        set_pass()

    password_e = base64.b64encode(bytes(password_d, encoding="utf-8"))
    print("Password set")

    dotenv.set_key(".env", "PASSWORD", password_e)

    load_env_variables()
    

    

# Resets the password and generates a new key
def reset(PASSWORD_D):

    """
    Resets the password and generates a new key

    Args:
        None

    Returns:
        None
    
    """

    key_gen(PASSWORD_D)
    default_d = "alpine"
    default_e = base64.b64encode(bytes(default_d, encoding="utf-8"))
    
    dotenv.set_key(".env", "PASSWORD", default_e)

    load_env_variables()

def managekeys(KEY_BACKUP):
    """
    Manages keys

    This function allows the user to perform various operations on encryption keys, such as backing up a key, deleting a backed up key, and restoring a backed up key as the current key.

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

                load_env_variables()
                break
            case 2:
                ask = input("Are you sure [y/n]]")
                if ask == "y":
                    dotenv.set_key(".env", "KEY_BACKUP", '')

                    load_env_variables()
                    break
            case 3:
                ask = input("Are you sure [y/n]")
                if ask == "y":
                    dotenv.set_key(".env", "KEY", KEY_BACKUP)
                    dotenv.set_key(".env", "KEY_BACKUP", '')

                    load_env_variables()
                    break
            case 0:
                break

def encrypt_file(KEY):

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


def decrypt_file(KEY, PASSWORD_D):
    
    """
    Decrypts a file

    Args:
        None
    
    Returns:
        None
    
    """

    if pass_check(PASSWORD_D) == True:
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
        pass_check(PASSWORD_D)

def debug_mode(PASSWORD_D, DEBUG):

    """
    Debug mode

    Args:
        None

    Returns:
        None

    """

    dotenv.load_dotenv()

    if pass_check(PASSWORD_D) == True:

        verfication = float(input("Please input the answer to this question: 8 / 2 * (2 + 2) = "))

    answer = 8 / 2 * (2 + 2)

    if verfication == answer:

        print("Verification successful")
    
    else:
        print("Verification failed")
        return



    state = validate_input("Input debug mode state [" + L_GREEN + "True" + RESET + "/" + L_RED + "False" + L_YELLOW + "]: ", str, "Please input True or False")

    dotenv.set_key(".env", "DEBUG", state)

    load_env_variables()

    if DEBUG == 'True':
        print("Debug mode", L_GREEN + "enabled" + RESET)

    elif DEBUG == 'False':
        print("Debug mode", L_RED + "disabled" + RESET)
        

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

if __name__ == "__main__":

    KEY, PASSWORD_E, PASSWORD_D, KEY_BACKUP, DEBUG = load_env_variables()

    if KEY == '':
        print("Either this is your first time running the script or YOU changed you key to '',no worries we are generating a new key for you.")
        print("Default password is 'alpine' you should change it after")
        key_gen(PASSWORD_D)

    # Controls the users choice throughout the script      
    while True:

        load_env_variables()

        choice = main()
        
        match choice:                                   # I use match statements because they are easier to read and more efficient than if statements

            case 1:
                encrypt = encrypt_func(KEY)
                print(encrypt)
            case 2:
                decrypt = decrypt_func(KEY, PASSWORD_D)
                print(decrypt)
            case 3:
                key_gen(PASSWORD_D)
            case 4:
                custom_key()
            case 5:
                key_print(KEY, PASSWORD_D)
            case 6:
                set_pass(PASSWORD_D)
            case 7:
                reset()
            case 8:
                managekeys(KEY_BACKUP)
            case 9:
                encrypt_file(KEY)
            case 10:
                decrypt_file(KEY, PASSWORD_D)
            case 0:
                debug_mode(PASSWORD_D, DEBUG)

        end()