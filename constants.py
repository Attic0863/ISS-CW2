import json

class Constants:
    @staticmethod # do not require creating class instance
    def get_encryption_key():
        with open('data/constants.json', 'r') as f:
            constants = json.load(f)
            return constants.get('encryption_key', None)
# This would not be used in a production scenario but since we are not using a database we are only working with json files for the design this will work
# in a production scenario we would use DB encryption with a key which is encrypted by the HSM