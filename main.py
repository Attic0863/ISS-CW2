# this file is the main entrypoint for the program which will use the different modules designed
from datetime import datetime
from encryption import Encryption
from authentication import Authentication

# this class allows the user to use all the modules and authentication
# role based access is done here to segment privileges based on their role, admin, doctor, patient
# admin role would have the most privileges and can view all records
# doctor role can view medical data and test results data for a patient
# a patient can view all their records and can put in financial information
def main():
    Encryption()
    authentication = Authentication()

    print("Welcome to the Medical Records System!")

    while True:
        print("\nPlease select your user type:")
        print("1. Admin")
        print("2. Doctor")
        print("3. Patient")
        print("4. Exit")

        user_choice = input("Enter your choice: ")

        if user_choice == "1":  # Admin
            admin_menu(authentication)
        elif user_choice == "2":  # Doctor
            doctor_menu(authentication)
        elif user_choice == "3":  # Patient
            patient_menu(authentication)
        elif user_choice == "4":  # Exit
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please select again.")

def admin_menu(auth):
    # we are going to assume that the admin is authenticated for the example but in a
    # real implementation the admin would have to login obviously
    print("\nAdmin Menu:")
    while True:
        print("\n1. View All Records")
        print("2. View Log")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nAll Records:")
            print("not implemented for now but this would go through all the records and showcase it")
            print("in a real implementation there would also be searching involved")
        elif choice == "2":
            log = auth.data_storage.view_log()
            print("\nLog File:")
            for record in log:
                print(record)
        elif choice == "3":
            print("Exiting Admin menu.")
            break
        else:
            print("Invalid choice. Please select again.")

def doctor_menu(auth):
    print("\nDoctor Menu:")
    doctor_session_token = login_or_register(auth, "doctor")
    # session tokens are used as a way to authenticate the user after they login once, session tokens in the real
    # implementation would expire after a certain time period forcing users to login again increasing security
    if doctor_session_token:
        while True:
            print("\n1. View Medical Records of a Patient")
            print("2. Create Medical Record for a Patient")
            print("3. Create Test Result for a Patient")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                patient_username = input("Enter patient's username: ")
                medical_records = auth.data_storage.get_all_medical_records(patient_username)
                if medical_records:
                    print("Medical records of", patient_username + ":")
                    print(medical_records)
                else:
                    print("No current medical records for", patient_username)

                test_results = auth.data_storage.get_all_test_results(patient_username)
                if test_results:
                    print("test results of", patient_username + ":")
                    print(test_results)
                else:
                    print("No current test results for", patient_username)
            elif choice == "2":
                patient_username = input("Enter patient's username: ")
                record = {
                    "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "diagnosis": input("Enter diagnosis: "),
                    "prescription": input("Enter prescription: ")
                }
                auth.data_storage.store_medical_record(patient_username, record)
                print("Medical record created successfully.")
            elif choice == "3":
                patient_username = input("Enter patient's username: ")
                result = {
                    "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "test_type": input("Enter test type: "),
                    "result": input("Enter test result: ")
                }
                auth.data_storage.store_test_result(patient_username, result)
                print("Test result created successfully.")
            elif choice == "4":
                print("Exiting Doctor menu.")
                break
            else:
                print("Invalid choice. Please select again.")

def patient_menu(auth):
    print("\nPatient Menu:")
    patient_session_token = login_or_register(auth, "patient")
    user = auth.get_user_from_session(patient_session_token)

    if patient_session_token:
        while True:
            print("\n1. View Medical Records and tests")
            print("2. View Financial Records")
            print("3. Enter Financial details")
            print("4. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                medical_records = auth.data_storage.get_all_medical_records(user.username)
                if medical_records:
                    print("Your medical records:")
                    print(medical_records)
                else:
                    print("No current medical records.")

                test_results = auth.data_storage.get_all_test_results(user.username)
                if test_results:
                    print("Your test results:")
                    print(test_results)
                else:
                    print("No current test results")
            elif choice == "2":
                financial_records = auth.data_storage.get_all_financial_records(user.username)
                if financial_records:
                    print("Your financial records:")
                    print(financial_records)
                else:
                    print("No current financial records.")
            elif choice == "3":
                financial_details = {
                    "income": input("Enter your income: "),
                    "expenses": input("Enter your expenses: "),
                    "savings": input("Enter your savings: ")
                }
                auth.data_storage.store_financial_record(user.username, financial_details)
                print("Financial details updated successfully.")
            elif choice == "4":
                print("Exiting Patient menu.")
                break
            else:
                print("Invalid choice. Please select again.")

# if this was a real implementation it would not be allowed to just register a doctor account without
# being verified or having some sort of procedure in place, for showcase purposes the
# system just allows registration of a doctor
def login_or_register(auth, user_role):
    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. Go Back")
        choice = input("Enter your choice: ")

        if choice == "1":  # Login
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            session_token = auth.login(username, password)
            if session_token:
                print(user_role.capitalize(), "logged in successfully.")
                return session_token
            else:
                print("Invalid username or password. Please try again.")
        elif choice == "2":  # Register
            username = input("Enter your desired username: ")
            password = input("Enter your password: ")
            session_token = auth.register(username, password, user_role)
            if session_token:
                print(user_role.capitalize(), "registered and logged in successfully.")
                return session_token
            else:
                print("Failed to register. Username may already exist.")
        elif choice == "3":  # Go back
            print("Going back to the main menu.")
            return None
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()
