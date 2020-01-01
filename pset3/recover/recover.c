#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define BLOCK_SIZE 512

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    BYTE data[512];
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: recover infile\n");
        return 1;
    }

    // open input file
    FILE *inptr = fopen(argv[1], "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open file\n");
        return 2;
    }

    char name[8];
    int number = 0;
    FILE *outptr = NULL;

    while (fread(data, sizeof(BYTE), BLOCK_SIZE, inptr) == 512)
    {
        //closing previous file if found a new
        if (data[0] == 0xff && data[1] == 0xd8 && data[2] == 0xff && (data[3] & 0xf0) == 0xe0 && outptr != NULL)
        {
            fclose(outptr);
            number = number + 1;
        }

        //start a new file whenever it is found

        if (data[0] == 0xff && data[1] == 0xd8 && data[2] == 0xff && (data[3] & 0xf0) == 0xe0)
        {
            sprintf(name, "%03i.jpg", number);
            outptr = fopen(name, "w");
        }

        // keep writing as we're parsing through the card
        if (outptr != NULL)
        {
            fwrite(data, sizeof(BYTE), 512, outptr);
        }
    }

     // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}