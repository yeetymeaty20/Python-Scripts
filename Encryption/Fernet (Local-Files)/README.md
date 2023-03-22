# Fernet Encryption & more

This script allows you to encrypt, decrypt and more with the Fernet package from cryptography 

Setup / Usage:
    When using this script at all time make sure to have to following in the same directory; "cipher.py", "thekey.key" & password.pass

Encryption:
    After the program outputs your encrypted text DO NOT copy the (b''), this is the formatting of the encryption only copy whats inside the the ''

Decryption:
    Same rules apply DO NOT copy the (b''), also as a WARNING if you want to actually use this then you need to keep your key safe and not generate a new one otherwise you wont be able to decrypt your encrypted text again

Key Gen:
    This creates a new key for you to use 

Custom Key:
    This is a very useful function as it allows you to reuse your old key for encryption again, so if you do plan on using this to encrypt something then i suggest writing dow your key found in "thekey.key"

Key Print:
    Prints out your key after you input the password, Alpine, by default I suggest changing it

Password Change:
    Allows you to change the password required to print out your key

Reset:
    This function is self explanatory it generates a new key and resets the password to Alpine, I will add a input function to ask if you are sure you want to continue in the future