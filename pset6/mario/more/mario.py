from cs50 import get_int


def get_positive_int(prompt):
    while True:
        n = get_int(prompt)
        if 0 < n < 9:
            break
    return n


def padding(g):
    for i in range(g):
        print(" ", end="")


def blocks(g):
    for i in range(g):
        print("#", end="")


Height = get_positive_int("Height: ")
Line = 1
for i in range(Height):
    padding(Height-Line)
    blocks(Line)
    print("  ", end="")
    blocks(Line)
    print()
    Line = Line + 1
