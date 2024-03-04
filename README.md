# Meditech System Simulation - 2248821

### Description:
This is a cryptographic simulation for MediTech Solutions: a Healthcare technology company.

### Assumptions:
- Using Json for storing data
- Having a master key to encrypt the files, in a real world scenario (production context) we would be using an SQL database
which is encrypted with a key that is essentially encrypted by the HSM
- In this implementation users are able to switch between admin, doctor and patient accounts and create them without 
verification, in a real production scenario a user would not be able to just access an admin account with no verification
or register as a doctor without verifying.
- The system right now assumes that the user does not want to login using something like microsoft SSO which in a real production
context there would be choice.

### GDPR Justification:
- Role-based Access is implemented
- Password Hashing SHA-512 + Salting
- Encryption at rest (AES)
- Encryption at transfer (RSA) + TLS
- Key Management allowing for key generation, rotation and retirement which maintains confidentiality and integrity of the keys.
- SSO Authentication (Username and password is used throughout the system)
- Comprehensive log of activities which helps accountability which complies with GDPR.
- User data handling allows for registration, modification and deletion following GDPR regulation

More details as comments in the code

### Usage (Python 3.10 was used):

```bash
pip install cryptography

pip install pyaes

pip install pbkdf2

python main.py
```
