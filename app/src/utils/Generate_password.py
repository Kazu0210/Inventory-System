import random
import string

class PasswordGenerator:
    def __init__(self):
        pass

    def password_generate(self, length):
        if length < 4:
            raise ValueError("Password length must be at least 4")

        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        numbers = string.digits
        all_chars = lowercase + uppercase + numbers
        
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(numbers),
        ]
        for _ in range(length - 3):
            password.append(random.choice(all_chars))
        
        random.shuffle(password)
        
        return ''.join(password)