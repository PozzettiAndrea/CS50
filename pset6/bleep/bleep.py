from cs50 import get_string
import sys

"""Checking for proper usage"""

if len(sys.argv) != 2:
    sys.exit("Usage: python bleep.py dictionary")

DICC = sys.argv[1]

words = set()
file = open(DICC, "r")
for line in file:
    words.add(line.rstrip("\n"))
file.close()

MSG = get_string("What message would you like to censor?\n")


def bleepybleep(n):
    Bleep = ""
    for i in range(n):
        Bleep += "*"
    return Bleep


def main():
    CENSORED = ""
    for word in MSG.split(" "):
        if word.lower() in words:
            CENSORED += bleepybleep(len(word)) + " "
        else:
            CENSORED += word + " "
    print(CENSORED)


if __name__ == "__main__":
    main()
