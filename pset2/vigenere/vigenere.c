#include <cs50.h>
#include <stdio.h>
#include <string.h>

int shift(char c);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }
    string codeword = argv[1];
    int i = 0;
    while (i < strlen(codeword))
        {
        if ((codeword[i] < 'A') || (codeword[i] > 'Z' && codeword[i] < 'a') || (codeword[i] > 'z'))
            {
            printf("Usage: ./vigenere keyword\n");
            return 1;
            }
        i = i + 1;
        }
    string message = get_string("plaintext: ");
    printf("ciphertext: ");
    int b = 0;
    int cshift = 0;
    while (b < strlen(message))
    {
        int key = shift(codeword[cshift%strlen(codeword)]);
        if (message[b] >= 'a' && message[b] <= 'z')
            {
            printf("%c", (((message[b] - 'a') + key) % 26) + 'a');
            cshift = cshift + 1;
            }
        else if (message[b] >= 'A' && message[b] <= 'Z')
            {
            printf("%c", (((message[b] - 'A') + key) % 26) + 'A');
            cshift = cshift + 1;
            }
        else
            {
            printf("%c", message[b]);
            }
        b = b + 1;
    }
    printf("\n");
    return 0;
}

int shift(char c)
{
    int shift = 0;
   if (c >= 'a' && c <= 'z')
       {
       shift = c - 'a';
       }
   if (c >= 'A' && c <= 'Z')
       {
       shift = c - 'A';
       }
   return shift;
}
