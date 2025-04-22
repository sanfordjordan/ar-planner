from typing import Literal
from typing import TypeVar, Iterable, Optional
T = TypeVar('T')

def set_user_value(user: Literal['B', 'J']):
    return user

#find item in array
def getThing(name: str, list: Iterable[T])-> Optional[T]:
   return next((thing for thing in list if thing.name == name), None)