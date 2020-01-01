from cs50 import get_int


CCNumber = get_int("Number: ")


def sum_digits(n):
    s = 0
    while n:
        s += n % 10
        n //= 10
    return s


"""First two digits and Length variables for later use"""
Length = len(str(CCNumber))
F2D = int(str(CCNumber)[:2])
FD = int(str(CCNumber)[0])


def LuhnsSum(Number):
    TOTALSUM = 0
    Length = len(str(Number))
    if (Length % 2) == 0:
        for i in range(Length//2):
            g = int((str(Number))[2*i])
            g = g * 2
            TOTALSUM += sum_digits(g)
        for i in range(Length//2):
            g = int((str(Number))[(2*i)+1])
            TOTALSUM += sum_digits(g)
    if (Length % 2) == 1:
        for i in range(Length//2):
            g = int((str(Number))[(2*i)+1])
            g = g * 2
            TOTALSUM += sum_digits(g)
        for i in range((Length//2)+1):
            g = int((str(Number))[2*i])
            TOTALSUM += sum_digits(g)

    if int((str(TOTALSUM))[-1]) == 0:
        return True
    else:
        return False


if(LuhnsSum(CCNumber)):
    if (Length == 15 and (F2D == 34 or F2D == 37)):
        print("AMEX")
    if (Length == 16 and (F2D == 51 or F2D == 52 or F2D == 53 or F2D == 54 or F2D == 55)):
        print("MASTERCARD")
    if ((Length == 13 or Length == 16) and (FD == 4)):
        print("VISA")

else:
    print("INVALID")