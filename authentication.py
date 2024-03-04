import json
from encryption import Encryption
from constants import Constants
from data_storage import DataStorage
from user import User
import uuid

# session tokens are used here and in the real implementation would expire after a certain time period but since this is
# a mock showcase it is not fully implemented here
class Authentication:
    def __init__(self):
        self.logged_in_users = {}
        self.encryption_key = Constants.get_encryption_key()
        self.encryption = Encryption()
        self.data_storage = DataStorage(self.encryption)

    def login_sso(self):
        # in this function microsoft sso would be utilised which means that the user can login using either microsoft
        # SSO or a username and password
        return

    # util methods
    def get_user_from_session(self, session_token):
        return self.logged_in_users[session_token]
    
    def _find_user_by_value(self, users, key, value):
        for user in users:
            if user.get(key) == value:
                return user
        return None

    # registers an account creating a salt and hashing the password to keep sensitive data secure
    def register(self, username, password, role):
        accounts = self.data_storage.read_data("users.json")["users"]

        if self._find_user_by_value(accounts, "username", username) is not None:
            return None # user exists

        salt = self._generate_uuid() ## uuids are secure and have a low collision rate, they are suitable to use in production and this mock implemntation

        # hash password
        hashed_password = self.encryption.hash_password(password, salt)

        newUser = {
            "username": username,
            "password": hashed_password,
            "salt": salt,
            "role": role
        }

        self.data_storage.add_user(newUser)

        return self.login(username, password)

    # sso authentication (username and password is used to login to everything)
    def login(self, username, password):
        accounts = self.data_storage.read_data("users.json")["users"]
        db_user = account = self._find_user_by_value(accounts, "username", username)

        if db_user is None: # user does not exist
            return None

        if self._check_password(password, db_user):
            session_token = self._generate_uuid()
            user = User(username, password, db_user["salt"], db_user["role"])
            self.logged_in_users[session_token] = user
            return session_token
        else:
            return None

    # when logging out remove session token from list of valid session tokens
    # to avoid access tokens being used after expiry and unnecessary risk
    def logout(self, session_token):
        if session_token in self.logged_in_users:
            del self.logged_in_users[session_token]
    
    def is_logged_in(self, session_token):
        return session_token in self.logged_in_users

    # check if inputted password matches the hash of the stored account
    def _check_password(self, password, stored_account):
        stored_hash = stored_account["password"]
        stored_salt = stored_account["salt"]

        hashed_password = self.encryption.hash_password(password, stored_salt)
        
        if hashed_password == stored_hash:
            return True
        else:
            return False

    # uuids have a dramatically low chance of collision and as such are suitable to use for session tokens
    def _generate_uuid(self):
        return str(uuid.uuid4())
