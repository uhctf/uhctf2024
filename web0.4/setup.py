import json
import random
import string

teams = [
    "Gibberende Git Goobers",
    "Firewall-fortifying File Fiddlers",
    "404 Name Not Found",
    "MaaS (Madness as a Solution)",
    "CTRL_F",
    "Flag Hunters",
    "failii++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>.>+++++.+++.---..",
    "skrinkly dinkles & ronny",
    "Ohh no, I got hacked!",
    "; DROP TABLE Teams; --",
    "Notworking",
    "Kris Code Compilet Niet",
    "404 Answer not found",
    "Snack Overflow",
    "Devin",
    "de nubs",
    "The Aphotics",
    "De rode lantaarn",
]

for team in teams:
    sanitizedname = "".join(e for e in team if e.isalnum())

    page = {
        "title": sanitizedname,
        "private": True,
        "body": team + "'s private page on the new and improved web!",
    }

    with open("wiki/pages/" + sanitizedname + ".json", "w") as fp:
        json.dump(page, fp)

    user = {
        "name": sanitizedname,
        "password": "".join(
            random.choice(string.ascii_lowercase + string.digits) for i in range(6)
        ),
        "level": 2,
        "pages": [sanitizedname],
    }

    with open("wiki/users/" + sanitizedname + ".json", "w") as fp:
        json.dump(user, fp)
