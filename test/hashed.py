from Hashpassword import HashPassword

needtoverifypass = "hatdog"
needtohashpass = "hatdog"

hash_password = HashPassword(needtohashpass)

hashedpass = hash_password.hash_password()
print(hashedpass)

verifyPass = HashPassword(needtoverifypass)
print(verifyPass.verify_password(hashedpass))