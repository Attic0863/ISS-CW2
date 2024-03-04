# the user has a role saved with it which will allow for different functions and access Patient role will only have
# access to view patient data related to them and only stuff necessary for them to use the system (no higher
# privileges) Doctor role will only have access patient data that is related to them and access to slightly elevated
# privileges Admin role will be able to view the most data and will have the most privileges (this role will only be
# given sparingly to site operatives and those who are, will only be able to be used onsite)

class User:
    def __init__(self, username, password, salt, role):
        self.username = username
        self.password = password
        self.salt = salt
        self.role = role

    def get_username(self):
        return self.username

    def get_role(self):
        return self.role
