import os
import base64
import shutil
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta

# in this class the private public keys for data transfer are generated and used and various functions to manage them.
# in the key management cycle it includes: generation, usage, rotating and retiring of keys which these functions showcase
# a mock implementation of in the system
class KeyManagement:
    def __init__(self, key_dir='keys'):
        self.key_dir = key_dir
        self._create_key_dir()

    # used to create
    def _create_key_dir(self):
        if not os.path.exists(self.key_dir):
            os.makedirs(self.key_dir)

    def generate_rsa_keypair(self, name):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()
        public_key_pem = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
        with open(os.path.join(self.key_dir, f'{name}_private.pem'), 'w') as f:
            f.write(private_key_pem)
        with open(os.path.join(self.key_dir, f'{name}_public.pem'), 'w') as f:
            f.write(public_key_pem)

    def load_rsa_public_key(self, name, user=None):
        if user:
            # Access control would be implemented here in a real implementation
            pass
        with open(os.path.join(self.key_dir, f'{name}_public.pem'), 'r') as f:
            return serialization.load_pem_public_key(f.read().encode(), backend=default_backend())

    def encrypt_with_public_key(self, public_key, data):
        encrypted_data = public_key.encrypt(
            data.encode(),
            padding.PKCS1v15()
        )
        return base64.b64encode(encrypted_data).decode()

    def decrypt_with_private_key(self, private_key, encrypted_data):
        decrypted_data = private_key.decrypt(
            base64.b64decode(encrypted_data),
            padding.PKCS1v15()
        )
        return decrypted_data.decode()

    def rotate_keys(self, name, backup_dir='key_backups'):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        backup_name = f'{name}_{timestamp}'
        shutil.copytree(self.key_dir, os.path.join(backup_dir, backup_name))
        self.generate_rsa_keypair(name)
        # we could also have it so old keys are deleted instead of backing them up

    def retire_keys(self, name, max_age_days=365):
        for file_name in os.listdir(self.key_dir):
            if file_name.startswith(name) and file_name.endswith("_private.pem"):
                file_path = os.path.join(self.key_dir, file_name)
                creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
                if datetime.now() - creation_time > timedelta(days=max_age_days):
                    os.remove(file_path)
