from os import getenv

import databases


user = getenv('DB_USER', 'postgres')
password = getenv('DB_PASS', 'postgres')
name = getenv('DATABASE_NAME', 'postgres')
hostname = getenv('DB_HOST', '127.0.0.1')
port = getenv('DB_PORT', 5432)
flavor = getenv('DATABASE', 'postgres')

url = f'{flavor}://{user}:{password}@{hostname}:{port}/{name}'
database = databases.Database(url)
del url, password
