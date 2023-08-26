import re


def snake_case_validator(name: str) -> str:
    pattern = r'^[a-z][a-z\d]*(_[a-z\d]+)*$'
    if re.search(pattern, name):
        return name
    raise ValueError('Name most follow snake_case rule.')
