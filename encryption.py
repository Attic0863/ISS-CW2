import pyaes, pbkdf2, binascii, os, secrets
import hashlib
import base64
from constants import Constants # import constants

# the encryption class facilitates the necessary encryption and hashing and salting for the users passwords when they
# register and ensures that the data is encrypted on rest for the system
class Encryption: 
    def __init__(self):
        self.encryption_key = pbkdf2.PBKDF2(Constants.get_encryption_key(), Constants.get_encryption_key()).read(32)
        self.iv = 105157905201001528579883136653745583962346817964095460216440166699768360247750
        # in production use the iv needs to be random but for the design we will use this for now
    
    def hash_password(self, password, salt=""): # sha512 to hash the passwords
        password = password.encode('utf-8')
        salt = salt.encode('utf-8')
        hashed_password = hashlib.pbkdf2_hmac('sha512', password, salt, 100000)
        return hashed_password.hex()

    def _base64_string(self, data):
        data_base64 = base64.b64encode(data).decode('utf-8')
        return data_base64
    
    def encrypt_data(self, data):
        key = self.encryption_key
        iv = self.iv
        aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
        ciphertext = aes.encrypt(data.encode())  # Ensure data is encoded to bytes before encryption
        return self._base64_string(ciphertext)

    def decrypt_data(self, encrypted_data):
        key = self.encryption_key
        iv = self.iv
        aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(iv))
        decrypted_bytes = aes.decrypt(base64.b64decode(encrypted_data))
        return decrypted_bytes.decode('utf-8')  # Decode bytes to string before returning
