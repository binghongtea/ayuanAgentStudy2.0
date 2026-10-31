from typing import TypedDict

# 声明类型字典
class Student(TypedDict):
    name: str
    age: int
    score: float

# 创建字典
student: Student = {
    "name": "小明",
    "age": 20,
    "score": 95.5
}

# 访问字典
print(student['name'])
print(student['age'])
print(student['score'])

# <class 'dict'>
print(type(student))

