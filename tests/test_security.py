import jwt
from backend.config import settings
from backend.security import create_access_token, hash_password, verify_password


hashed = hash_password('secret123')
print(f'Hashed Password :{hashed}')
print(verify_password('secret123', hashed))  # right password
print(verify_password('wrong', hashed))
# wrong password
token = create_access_token('maria')
print(jwt.decode(token, settings.secret_key, algorithms=['HS256']) )