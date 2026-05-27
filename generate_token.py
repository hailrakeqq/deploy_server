import secrets

token = secrets.token_hex(32)

with open('.env', "w") as file:
    file.write(f'API_TOKEN={token}')
