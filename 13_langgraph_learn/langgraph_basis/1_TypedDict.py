from typing import TypedDict

class Student(TypedDict):
    name: str
    age: int
    score: float

student: Student = {
    "name": "小明",
    "age": 20,
    "score": 95.5
}

print(student["name"])
print(student["score"])
print(type(student))