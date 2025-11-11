# a simple way of registering and verifying users in a hopefully secure way
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import hashlib


def register(name, password):
    print(f'registering {name} with password {password}')
    # hashing
    passhash = hashlib.sha256(password.encode('utf8')).hexdigest()
    # TODO remove before production
    print(f'{name} with password {passhash}')
    password = passhash
    return passhash


def verify(hashed, entered_password):
    # hash password
    passhash = hashlib.sha256(entered_password.encode('utf8')).hexdigest()
    if passhash == hashed:
        return True
    return False

# TODO remove debug statements