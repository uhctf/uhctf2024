import colorama
import re
from dns import resolver as rslv
from dns.rdatatype import RdataType
from dns.resolver import Answer
from typing import List
import os

# Setup client with correct server
resolver = rslv.Resolver(configure=False)
resolver.nameservers = ["34.38.129.6"]
resolver.port = 5353


def query(typ: str, domain: str, ignore_fail: bool = False) -> Answer:
    global resolver
    return resolver.resolve(domain, typ, raise_on_no_answer=not ignore_fail)


# Create a game: get a UUID
uuid_re = re.compile(r'([a-f0-9]+)\.dnstris\.ctf.')
uuid_response = query('A', 'dnstris.ctf.')
uuid = None
for reply in uuid_response.response.answer:
    mtch = re.fullmatch(uuid_re, reply.name.__str__())
    if mtch is not None:
        uuid = mtch[1]
        break
print(f"uuid set to {uuid}")

board = []
info = ""
score = 0
nxt = []
hold = []


def update_field(input: str, width: int):
    """Converts the given input (provided by the server) and prints it nicely"""
    new_field = []
    idx = 0
    while idx < len(input):
        new_field += [input[idx:idx+width]]
        idx += width
    return new_field


def print_field(inp: List[str]):
    """Prints the given field using colors."""
    from termcolor import colored
    # What to print, coloe, background color

    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        YELLOW = '\033[33m'
        PURPLE = '\033[95m'
        RED = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    mapping = {
        ' ': (' ', bcolors.OKCYAN, bcolors.ENDC),
        'I': ('█', bcolors.OKCYAN, bcolors.ENDC),
        'J': ('█', bcolors.OKBLUE, bcolors.ENDC),
        'L': ('█', bcolors.WARNING, bcolors.ENDC),
        'O': ('█', bcolors.YELLOW, bcolors.ENDC),
        'S': ('█', bcolors.OKGREEN, bcolors.ENDC),
        'T': ('█', bcolors.PURPLE, bcolors.ENDC),
        'Z': ('█', bcolors.RED, bcolors.ENDC),
        'x': ('▒', bcolors.OKCYAN, bcolors.ENDC)
    }
    for line in inp:
        for chaar in line:
            mapped = mapping[chaar]
            print(mapped[1], mapped[0], mapped[2], sep="", end="")
        print()


def update_board(new_input: str):
    global board
    width = 10
    new_board = update_field(new_input, width)
    board = new_board


def update_nxt(new_input: str):
    global nxt
    width = 4
    new_nxt = update_field(new_input, width)
    nxt = new_nxt


def update_hold(new_input: str):
    global hold
    width = 4
    new_hold = update_field(new_input, width)
    hold = new_hold


def update_score(new_score: str):
    global score
    score = int(new_score)


def update_info(new_info: str):
    global info
    info = new_info


def show_board():
    global board
    for line in board:
        print(line)


def show_board():
    global board
    for line in board:
        print(line)


def show_hold():
    global hold
    for line in hold:
        print(line)


def show_nxt():
    global nxt
    for line in nxt:
        print(line)


# Keep updating the board and other stuff
while info != "game over!":
    status_domain = f"{uuid}.dnstris.ctf."
    status_response = query('TXT', status_domain)

    for answer in status_response.response.answer:
        if answer.rdtype != RdataType.TXT:
            # Skip that one A record
            continue

        for answer in answer.items:
            answer = str(answer)[1:-1].split("=")
            key = answer[0]
            value = answer[1]
            if key == "board":
                update_board(value)
            elif key == "score":
                update_score(value)
            elif key == "info":
                update_info(value)
            elif key == "next":
                update_nxt(value)
            elif key == "holding":
                update_hold(value)
            else:
                from sys import exit
                print(f"unexpected key {key}")
                exit(1)

    # Output of the update
    print_field(board)
    print("-"*10)
    print("HOLD")
    print_field(hold)
    print("NEXT")
    print_field(nxt)
    print(f"score  {score}")
    print(f"info   {info}")

    # Read input to perform an action
    print("command or enter? WASD A: left, D: right, S: down, W: rotate, e: drop, q: hold/swap, Enter: refresh")
    inpt = input(" > ")
    cmd = None

    if inpt == "a":
        cmd = "left"
    if inpt == "d":
        cmd = "right"
    if inpt == "w":
        cmd = "rotate"
    if inpt == "e":
        cmd = "drop"
    if inpt == "q":
        cmd = "hold"
    if inpt == 's':
        cmd = "down"

    if cmd is None:
        if inpt != "":
            print("invalid command")
    else:
        # No need to wait for a response
        query('TXT', f"{cmd}.{status_domain}", True)
