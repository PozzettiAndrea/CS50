from cs50 import get_string
import sys


"""Checking for proper usage"""

if len(sys.argv) != 2:
    sys.exit("Usage: python vigenere.py k")

if not sys.argv[1].isalpha():
    sys.exit("Usage: python vigenere.py k")


Key = sys.argv[1].lower()


"""Building an alphabet list and a letter-->number dictionary for later"""

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
            "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

alpha_dict = {letter: idx for idx, letter in enumerate(alphabet)}

MSG = get_string("plaintext: ")
ITL = len(Key)
MSG2 = ""
space = 0

for i in range(len(MSG)):
    if MSG[i] == " ":
        space += 1
    if MSG[i].isalpha():
        if MSG[i].isupper():
            MSG2 += alphabet[(alpha_dict[MSG[i].lower()] + alpha_dict[Key[(i + space) % ITL]]) % 26].upper()
        else:
            MSG2 += alphabet[(alpha_dict[MSG[i]] + alpha_dict[Key[(i + space) % ITL]]) % 26]

    else:
        MSG2 += MSG[i]

print("ciphertext:", MSG2)
