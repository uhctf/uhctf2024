import hashlib
from sys import exit

HASH = "69edd447655e95cf4ad0e987e14e0c97d8aca399a8681d8be1062bbb8030515ce48ba58b8da4e02164785a947b4e4fa0f946185f05d4f18150d0cd76452ea60c"

for number in range(1_000_000_000):
    string = f"{number}".rjust(9,"0")
    print(string, end="\r")
    if hashlib.sha512(bytes(string, "utf-8")).hexdigest() == HASH:
        print(string)
        exit(0)
