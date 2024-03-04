import os
import json
import datetime
from encryption import Encryption  # import the Encryption class

# throughout this module encryption and decryption is used to ensure that the files are kept secure on rest
# symmetric encryption was chosen for data at rest and for data transfer tls and asymmetrical encryption will be used
# this system also allows for editing of data and deletion of users accounts
class DataStorage:
    def __init__(self, encryption_obj, data_dir='data'):  # use encryption object as argument
        self.data_dir = data_dir
        self.encryption = encryption_obj
        self.log_file = os.path.join(self.data_dir, 'log.json')
        self.user_file = os.path.join(self.data_dir, 'users.json')
        self._create_log_file()
        self._create_user_file()

    def _create_log_file(self):
        if os.path.exists(self.log_file) == False:
            initial_data = json.dumps([])
            encrypted_data = self.encryption.encrypt_data(initial_data)
            with open(self.log_file, 'w') as file:
                file.write(encrypted_data)

    def _create_user_file(self):
        if os.path.exists(self.user_file) == False:
            initial_data = json.dumps({"users": []})
            encrypted_data = self.encryption.encrypt_data(initial_data)
            with open(self.user_file, 'w') as file:
                file.write(encrypted_data)

    def _write_log(self, operation, filename, context=""):
        decrypted_data = None
        with open(self.log_file, 'r') as file:
            encrypted_data = file.read()
            decrypted_data = self.encryption.decrypt_data(encrypted_data)
        
        log_entries = json.loads(decrypted_data) if decrypted_data else []
        timestamp = datetime.datetime.now().isoformat()
        log_entry = {'timestamp': timestamp, 'operation': operation, 'filename': filename, 'context': context}
        log_entries.append(log_entry)

        encrypted_log_entry = self.encryption.encrypt_data(json.dumps(log_entries))
        with open(self.log_file, 'w') as file:
            file.write(encrypted_log_entry)

    def write_data(self, filename, data, context):
        encrypted_data = self.encryption.encrypt_data(data)
        with open(os.path.join(self.data_dir, filename), 'w') as file:
            file.write(encrypted_data)
        self._write_log('write_data', filename, context)

    def read_data(self, filename):
        with open(os.path.join(self.data_dir, filename), 'r') as file:
            encrypted_data = file.read()
            decrypted_data = self.encryption.decrypt_data(encrypted_data)
            self._write_log("read", filename)
            return json.loads(decrypted_data)

    def add_user(self, new_user):
        with open(self.user_file, 'r') as file:
            encrypted_users = file.read()
        decrypted_users = self.encryption.decrypt_data(encrypted_users)

        users_data = json.loads(decrypted_users)
        users_data['users'].append(new_user)

        encrypted_users_data = self.encryption.encrypt_data(json.dumps(users_data))

        with open(self.user_file, 'w') as file:
            file.write(encrypted_users_data)
        self._write_log("registration", "users.json", new_user["username"])

    def _get_data(self, folder, filename):
        directory = os.path.join(self.data_dir, folder)
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, filename)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write(self.encryption.encrypt_data(json.dumps([])))
        with open(file_path, 'r') as file:
            encrypted_data = file.read()
        if encrypted_data == "":
            return None
        return json.loads(self.encryption.decrypt_data(encrypted_data))

    def _store_data(self, folder, filename, data):
        directory = os.path.join(self.data_dir, folder)
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, filename)

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                encrypted_data = file.read()
            decrypted_data = self.encryption.decrypt_data(encrypted_data)
            existing_data = json.loads(decrypted_data)
        else:
            existing_data = []

        existing_data.append(data)

        with open(file_path, 'w') as file:
            file.write(self.encryption.encrypt_data(json.dumps(existing_data)))


    def store_record(self, folder, filename, record):
        self._store_data(folder, filename, record)
        self._write_log("store_record", filename, record)

    def get_all_records(self, folder, filename):
        data = self._get_data(folder, filename)
        self._write_log("get_all_records", filename)
        return data

    def store_financial_record(self, patient_username, record):
        folder = 'finance'
        filename = f'financial_records_{patient_username}.json'
        self.store_record(folder, filename, record)

    def get_all_financial_records(self, patient_username):
        folder = 'finance'
        filename = f'financial_records_{patient_username}.json'
        return self.get_all_records(folder, filename)

    def store_medical_record(self, patient_username, record):
        folder = 'record'
        filename = f'medical_records_{patient_username}.json'
        self.store_record(folder, filename, record)

    def get_all_medical_records(self, patient_username):
        folder = 'record'
        filename = f'medical_records_{patient_username}.json'
        return self.get_all_records(folder, filename)

    def store_test_result(self, patient_username, result):
        folder = 'tests'
        filename = f'test_results_{patient_username}.json'
        self.store_record(folder, filename, result)

    def get_all_test_results(self, patient_username):
        folder = 'tests'
        filename = f'test_results_{patient_username}.json'
        return self.get_all_records(folder, filename)

    def get_all_records_in_folder(self, folder):
        records = []
        directory = os.path.join(self.data_dir, folder)

        if os.path.exists(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    records.extend(self._get_data(folder, filename))

        self._write_log("get_all_records_in_folder", folder)
        return records

    def get_every_record(self):
        records = {}
        for folder in ['record', 'tests', 'finance']:
            records[folder] = self.get_all_records_in_folder(folder)
        return records

    # this will allow for the satisfying of editing data in gdpr regulation
    # not fully functioning but a mock implementation of it
    def edit_record(self, folder, filename, record_id, new_data):
        records = self._get_data(folder, filename)

        for record in records:
            if record.get('id') == record_id:
                record.update(new_data)
                break

        with open(os.path.join(self.data_dir, folder, filename), 'w') as file:
            file.write(self.encryption.encrypt_data(json.dumps(records)))

        self._write_log("edit_record", filename, f"Record ID: {record_id}")

    def delete_account(self, username, password):
        return
        # authentication would be done here and then the account data would be deleted
        # e.g. financial records, medical records, tests, and the user would be wiped from the users.json file

    # decrypts the log file so the admin can view it, this lets the admin see if there is any suspicious activity
    # further enhancing the security of the system
    def view_log(self):
        with open(self.log_file, 'r') as file:
            encrypted_data = file.read()
            decrypted_data = self.encryption.decrypt_data(encrypted_data)
            return json.loads(decrypted_data)