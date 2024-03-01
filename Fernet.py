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

default_e = "YWxwaW5l"

def loadEnvVariables():

    if load_dotenv(dotenv_path=".env") == False:
        print(L_RED + "No .env file found, creating one for you." + RESET)
        with open(".env", "w") as file:
            file.close()

        load_dotenv(dotenv_path=".env")
        os.environ.clear()
        dotenv.set_key(".env", "PASSWORD", default_e)
        dotenv.set_key(".env", "DEBUG", "False")
        dotenv.set_key(".env", "KEY_BACKUP", "")
        dotenv.set_key(".env", "KEY", "")

    

    os.environ.clear()
    load_dotenv(dotenv_path=".env")
    KEY = os.getenv("KEY")
    PASSWORD_E = os.getenv("PASSWORD")
    PASSWORD_D = base64.b64decode(PASSWORD_E).decode("utf-8", "strict")
    KEY_BACKUP = os.getenv("KEY_BACKUP")

    DEBUG = os.getenv("DEBUG")

    return KEY, PASSWORD_E, PASSWORD_D, KEY_BACKUP, DEBUG

def validateInput(prompt, expected_type, error_message):
    while True:
        user_input = input(L_YELLOW + prompt + RESET)
        try:
            user_input = expected_type(user_input)
            return user_input
        except ValueError:
            print(L_RED + error_message + RESET)


loadEnvVariables()

# Asks users for their password
def passCheck(PASSWORD_D):

    """
    Asks the user for password and checks if it is correct
    
    Args:
        PASSWORD_D (str): password
    
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

    choice = validateInput("Input a number: ", int, "Please input a number")

    try:
        choice = int(choice)
        return choice
    except ValueError:
        print(L_RED + "Please input a number" + RESET)

    

# Encrypt function
def encryptFunc(KEY):

    """
    Encrypts the text the user inputs

    Args:
        KEY (str): encryption key

    Returns:
        str: encrypted text

    """

    text = validateInput("Input text: ", str, "Please input text")

    data = bytes(text, encoding="utf-8")
    encryption_tool = Fernet(KEY)
    encrypted = encryption_tool.encrypt(data)

    return(str(encrypted))

# Decrypt function
def decryptFunc(KEY, PASSWORD_D):
    """
    Decrypts the text the user inputs

    Args:
        KEY (str): encryption key
        PASSWORD_D (str): password

    Returns:
        str: decrypted text
    """

    if passCheck(PASSWORD_D) == True:

        data = validateInput("Input text: ", str, "Please input text")

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
        passCheck(PASSWORD_D)


# Key generation
def keyGen(PASSWORD_D):

    """
    Generates a new key and saves it to .env file

    Args:
        PASSWORD_D (str): password
    
    Returns:
        None
    
    """

    if passCheck(PASSWORD_D) == True:

        key = Fernet.generate_key()
        key_str = key.decode("utf-8", "strict")

        dotenv.set_key(".env", "KEY", key_str)

        loadEnvVariables()
        print("Key generated")

    else:
        passCheck(PASSWORD_D)

# Import custom keys so you can share encrypted messages with others
def customKey(PASSWORD_D):

    """
    Imports a custom key and saves it to .env file

    Args:
        PASSWORD_D (str): password

    Returns:
        None
    
    """

    if passCheck(PASSWORD_D) == True:

        key = input("Input key: ")
        key = bytes(key, encoding="utf-8")
        key_str = key.decode("utf-8", "strict")
        dotenv.set_key(".env", "KEY", key_str)

        loadEnvVariables()     
    else:
        passCheck(PASSWORD_D)

def outputKey(KEY, PASSWORD_D):

    """
    Prints out the current key

    Args:
        KEY (str): encryption key
        PASSWORD_D (str): password

    Returns:
        None

    """
    
    if passCheck(PASSWORD_D) == True:
        print(KEY)
    else:
        passCheck(PASSWORD_D)

# Changes password
def setPswd(PASSWORD_D):

    """
    Changes the password

    Args:
        PASSWORD_D (str): password

    Returns:
        None
    
    """
    
    print("Warning for security reasons this will reset your key as well so you cant access someone elses encryptions by resetting password.")
    keyGen(PASSWORD_D)

    password_d = input("Input new Password: ")
    double_check = input("Input new Password again: ")

    if password_d != double_check:
        print("Passwords do not match")
        setPswd(PASSWORD_D)

    password_e = base64.b64encode(bytes(password_d, encoding="utf-8"))
    print("Password set")

    dotenv.set_key(".env", "PASSWORD", password_e.decode("utf-8", "strict"))
        




    loadEnvVariables()
    

    

# Resets the password and generates a new key
def reset(PASSWORD_D):

    """
    Resets the password and generates a new key

    Args:
        PASSWORD_D (str): password

    Returns:
        None
    
    """

    keyGen(PASSWORD_D)
    default_d = "alpine"
    default_e = base64.b64encode(bytes(default_d, encoding="utf-8"))
    
    dotenv.set_key(".env", "PASSWORD", default_e)

    loadEnvVariables()

def manageKeys(KEY_BACKUP):
    """
    Manages keys

    This function allows the user to perform various operations on encryption keys, such as backing up a key, deleting a backed up key, and restoring a backed up key as the current key.

    Args:
        KEY_BACKUP (str): backed up key
    
    Returns:
        None
    """
    while True:
        print("1. Backup a key")
        print("2. Delete backed up key")
        print("3. Restore backed up key as current key")
        print("0. Go back to main menu")
        option_key = validateInput("Input a number: ", int, "Please input a number")

        match option_key:
            case 1:
                if KEY_BACKUP != '':
                    print("Delete this backed up key first")

                backedupkey = input("Input the key: ")
                dotenv.set_key(".env", "KEY_BACKUP", backedupkey)

                loadEnvVariables()
                break
            case 2:
                ask = input("Are you sure [y/n]]")
                if ask == "y":
                    dotenv.set_key(".env", "KEY_BACKUP", '')

                    loadEnvVariables()
                    break
            case 3:
                ask = input("Are you sure [y/n]")
                if ask == "y":
                    dotenv.set_key(".env", "KEY", KEY_BACKUP)
                    dotenv.set_key(".env", "KEY_BACKUP", '')

                    loadEnvVariables()
                    break
            case 0:
                break

def encryptFile(KEY):

    """
    Encrypts a file

    Args:
        KEY (str): encryption key
    
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


def decryptFile(KEY, PASSWORD_D):
    
    """
    Decrypts a file

    Args:
        KEY (str): encryption key
        PASSWORD_D (str): password
    
    Returns:
        None
    
    """

    if passCheck(PASSWORD_D) == True:
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
        passCheck(PASSWORD_D)

def debugMode(PASSWORD_D, DEBUG):

    """
    Debug mode

    Args:
        PASSWORD_D (str): password
        DEBUG (str): debug mode state

    Returns:
        None

    """

    dotenv.load_dotenv()

    if passCheck(PASSWORD_D) == True:

        verfication = float(input("Please input the answer to this question: 8 / 2 * (2 + 2) = "))

    answer = 8 / 2 * (2 + 2)

    if verfication == answer:

        print("Verification successful")
    
    else:
        print("Verification failed")
        return



    state = validateInput("Input debug mode state [" + L_GREEN + "True" + RESET + "/" + L_RED + "False" + L_YELLOW + "]: ", str, "Please input True or False")

    dotenv.set_key(".env", "DEBUG", state)

    loadEnvVariables()

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

    KEY, PASSWORD_E, PASSWORD_D, KEY_BACKUP, DEBUG = loadEnvVariables()

    if KEY == "" or KEY == None or PASSWORD_D == "alpine" or PASSWORD_D == None or PASSWORD_D == "":
        print("Either this is your first time running the script or YOU changed you key to '',no worries we are generating a new key for you.")
        print("Default password is 'alpine' you will be prompted to change it after the key is generated.")
        keyGen(PASSWORD_D)
        print("Please change your password")
        setPswd(PASSWORD_D)
        
            

    # Controls the users choice throughout the script      
    while True:

        KEY, PASSWORD_E, PASSWORD_D, KEY_BACKUP, DEBUG = loadEnvVariables()

        choice = main()
        
        match choice:                                   # I use match statements because they are easier to read and more efficient than if statements

            case 1:
                encrypt = encryptFunc(KEY)
                print(encrypt)
            case 2:
                decrypt = decryptFunc(KEY, PASSWORD_D)
                print(decrypt)
            case 3:
                keyGen(PASSWORD_D)
            case 4:
                customKey()
            case 5:
                outputKey(KEY, PASSWORD_D)
            case 6:
                setPswd(PASSWORD_D)
            case 7:
                reset()
            case 8:
                manageKeys(KEY_BACKUP)
            case 9:
                encryptFile(KEY)
            case 10:
                decryptFile(KEY, PASSWORD_D)
            case 0:
                debugMode(PASSWORD_D, DEBUG)

        end()