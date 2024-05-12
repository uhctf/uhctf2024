import itertools
from random import shuffle, seed

WORDS = [
    ["Duvel", "Limburg.net", "Xz", "Edpnet"],
    # Non-pentesting distros
    ["Arch","Ubuntu","Fedora","NixOS"],
    ["C++","Go(lang)","Rust","TypeScript"],
    ["Spear-phishing", "DDoS", "Tor (network)", "Deepfake"],
    ["The Pirate Bay","1337","Rickroll","Pepe"]
]

LIST_NAMES = ["Recent data breach/exploit", "Non-pentesting distro", "Programming Language, not used at the CTF", "Generic cybersecurity term", "Internet culture"]


ALL_WORDLIST = list(itertools.product(*WORDS))

# Mix them a bit
seed(123456)
shuffle(ALL_WORDLIST)

# Taking the team id for reproducability
TEAM_COUNT = 100
ALL_WORDLIST = ALL_WORDLIST[:TEAM_COUNT]
for i, words in enumerate(ALL_WORDLIST):
    if i < 74:
        continue
    print("Dear TEAM {}".format(i))
    print("Your codewords are:")
    for word, category in zip(words, LIST_NAMES):
        print("||{}|| (category ||{}||)".format(word, category))
    print("Every team has one word of each category to make it fair.")
    print("If you can make a CTF crew member say one of these words, ask them for the flag.")
    print()
