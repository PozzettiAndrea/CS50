#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    int key = atoi(argv[1]);
    string message = get_string("plaintext: ");
    printf("ciphertext: ");
    int i = 0;
    while (i < strlen(message))
    {
        if (message[i] >= 'a' && message[i] <= 'z')
            {
            printf("%c", (((message[i] - 'a') + key) % 26) + 'a');
            }
        else if (message[i] >= 'A' && message[i] <= 'Z')
            {
            printf("%c", (((message[i] - 'A') + key) % 26) + 'A');
            }
        else
            {
            printf("%c", message[i]);
            }
        i = i + 1;
    }
    printf("\n");
    return 0;
}
