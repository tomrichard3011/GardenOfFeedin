import secrets
from gardenApp.models import PublicUser
from django.contrib.auth.hashers import PBKDF2PasswordHasher, check_password


'''
Hashes a string
Using PBKDF2 with 32 byte salt
Returns string of password hash
'''
def hashPassword(plaintext):
    # hash password
    # random salt generation - 32 bytes should be secure enough
    uniqueSalt = secrets.token_urlsafe(32)
    passwordHash = PBKDF2PasswordHasher.encode(
        self=PBKDF2PasswordHasher,
        password=plaintext,
        salt=uniqueSalt
    )
    return passwordHash


'''
Checks the validity of a user in the local database.
routes based on validity of credentials
'''
def userLoginAuthentication(email, password):
    try:
        user = PublicUser.objects.get(email=email)
    except Exception as e:
        print(e)
        return False
    if user is None:
        raise Exception("No such user")
    return check_password(password, user.pass_hash)
