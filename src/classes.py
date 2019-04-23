from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from tqdm import tqdm  # Progress bar

from threading import Thread
from src.functions import secure_delete


class Colors:
    bold = "\033[1m"
    underline = "\033[4m"
    blue = "\033[94m"
    red = "\033[91m"
    green = "\033[92m"


class AesExcalibur:
    """Class used to encrypt and decrypt data"""

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
        try:
            with open(file_name, 'rb') as f:
                plain_text = f.read()
            encrypted = self.encrypt(plain_text)
            with open(file_name + ".AeS", 'wb+') as f:
                f.write(encrypted)
            secure_delete(file_name)  # Delete original
        except (IOError, ValueError, FileNotFoundError, Exception):
            pass  # Suppress output for progress bars

    def decrypt_file(self, file_name):
        try:
            with open(file_name, 'rb') as f:
                cipher_text = f.read()
            decrypted = self.decrypt(cipher_text)
            with open(file_name[:-4], 'wb+') as f:
                f.write(decrypted)
            secure_delete(file_name)
        except (IOError, ValueError, FileNotFoundError) as err:
            print(Colors.red + "An error occured: {}".format(err))


class AsyncEncrypt(Thread):
    """Start a thread that encrypts an array of files"""

    def __init__(self, encryption_object, file_list):
        Thread.__init__(self)
        self.crypt = encryption_object
        self.files = file_list
        self.daemon = True

    def run(self):
        for file in tqdm(self.files, ascii=True, smoothing=0.8, desc="Encryption status: {}".format(self.name)):
            self.crypt.encrypt_file(file)