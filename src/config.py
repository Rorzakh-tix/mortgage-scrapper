from dotenv import load_dotenv

import os

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")


DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")


# DB_HOST_TEST = os.environ.get("DB_HOST_TEST")
# DB_PORT_TEST = os.environ.get("DB_PORT_TEST")
# DB_NAME_TEST = os.environ.get("DB_NAME_TEST")
# DB_USER_TEST = os.environ.get("DB_USER_TEST")
# DB_PASS_TEST = os.environ.get("DB_PASS_TEST")

AWS_SECRET = os.environ.get("AWS_SECRET")
AWS_ACCESS = os.environ.get("AWS_ACCESS")
