from typing import TypedDict


class User(TypedDict):
    name: str
    age: int

user: User = {"name": "maker", "age": 2}
print(user)
print(user["name"])
print(user["age"])
