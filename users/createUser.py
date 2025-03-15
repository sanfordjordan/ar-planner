import importlib
import sys

from typing import Literal
from Objects.userObject import User

def createUser(user: Literal['B', 'J']) -> User:
    module_name = user
    sys.path.append('users')
    module = __import__(module_name)
    a = {key: value for key, value in module.__dict__.items() if not key.startswith('__')}
    return User(
    a['name'], 
    a['weight'], 
    a['sweatLevel'], 
    a['kayakFood'], 
    a['hikeFood'], 
    a['bikeFood'],
    a['foodFormula'],
    )
