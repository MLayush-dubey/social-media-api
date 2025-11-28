from pwdlib import PasswordHash
hashpassword = PasswordHash.recommended()  

#hash a password
def hashing(password: str):
    return hashpassword.hash(password)


#creating a function for comparing user password with our hashed database password
def verify(user_password, hashed_password):
    return hashpassword.verify(user_password, hashed_password)