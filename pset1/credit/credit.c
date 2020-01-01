#include <cs50.h>
#include <stdio.h>
#include <math.h>

long long CNUMBER;

int main(void)
{do
{
CNUMBER = get_long("Please enter your credit card number here\n");
}
while (CNUMBER <= 0);

double kindalength = log10(CNUMBER);
int length = floor(kindalength) + 1;
int Digits[length];
int i = 0;
while (i < length)
    {int f = CNUMBER % 10;
    Digits[i] = f;
    CNUMBER = CNUMBER/10;
    i = i + 1;
    }
int b = 0;
int DoubleDigSum[length];
 while (b < length)
       {
    DoubleDigSum[b] = (Digits[b]*2);
    DoubleDigSum[b] = (DoubleDigSum[b] % 10) + DoubleDigSum[b]/10;
    b = b + 1;
    }
int totalsum;
if (length == 16)
      {
    totalsum = DoubleDigSum[1]+DoubleDigSum[3]+DoubleDigSum[5]+DoubleDigSum[7]+DoubleDigSum[9]+DoubleDigSum[11]+DoubleDigSum[13]+DoubleDigSum[15]+Digits[0]+Digits[2]+Digits[4]+Digits[6]+Digits[8]+Digits[10]+Digits[12]+Digits[14];
    }
if (length == 15)
      {
    totalsum = DoubleDigSum[1]+DoubleDigSum[3]+DoubleDigSum[5]+DoubleDigSum[7]+DoubleDigSum[9]+DoubleDigSum[11]+DoubleDigSum[13]+Digits[0]+Digits[2]+Digits[4]+Digits[6]+Digits[8]+Digits[10]+Digits[12]+Digits[14];
    }
if (length == 13)
      {
    totalsum = DoubleDigSum[1]+DoubleDigSum[3]+DoubleDigSum[5]+DoubleDigSum[7]+DoubleDigSum[9]+DoubleDigSum[11]+Digits[0]+Digits[2]+Digits[4]+Digits[6]+Digits[8]+Digits[10]+Digits[12];
    }
if (totalsum%10 == 0 && (length == 16 || length == 15 || length == 13))
{switch (Digits[length-1])
 {case 5:
  if(Digits[length-2] == 1 || Digits[length-2] == 2 || Digits[length-2] == 3 || Digits[length-2] == 4 || Digits[length-2] == 5)
  {
  printf("MASTERCARD\n");
  } else { printf("INVALID\n");
    }
  break;
  case 4:
  printf("VISA\n");
  break;
  case 3:
  if(Digits[length-2] == 4 || Digits[length-2] == 7)
  {
  printf("AMEX\n");
  } else { printf("INVALID\n");
    }
  break;
 }
 }
else 
  { printf("INVALID\n");
    }
 
}
