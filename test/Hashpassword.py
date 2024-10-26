import hashlib
import binascii
import os

class HashPassword:
    def __init__(self, password):
        if not password:
            raise ValueError("Password cannot be empty")
        self.password = password

    def hash_password(self):
        """Hash a password for storing."""
        salt_length = 60
        salt = hashlib.sha256(os.urandom(salt_length)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha256', self.password.encode('utf-8'), 
                                      salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    def verify_password(self, stored_password):
        """Verify a stored password against one provided by user"""
        if not stored_password:
            raise ValueError("Stored password cannot be empty")
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha256', self.password.encode('utf-8'), salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

    def update_password(self, new_password):
        """Update the password"""
        self.password = new_password
        return self.hash_password()

    def is_valid_password(self):
        """Check if the password is valid"""
        # Add your password validation logic here
        # For example:
        if len(self.password) < 8:
            return False
        if not any(char.isdigit() for char in self.password):
            return False
        if not any(char.isupper() for char in self.password):
            return False
        return True
    

    