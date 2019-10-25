#
# create a crypt context that can be imported and used wherever is needed...
# the instance will be configured later.
#
from passlib.context import CryptContext
user_pwd_context = CryptContext()
