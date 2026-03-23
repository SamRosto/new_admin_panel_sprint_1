import os
from dotenv import load_dotenv

load_dotenv()

DBNAME = "movies_database" # os.environ.get('DBNAME')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD')
HOST = os.environ.get('HOST')
PORT = os.environ.get('PORT')
