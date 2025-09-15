#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    // The program must accept one command-line argument which is the name of forensic image
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("file not openeing");
        return 2;
    }
    uint8_t Buffer[BLOCK_SIZE];
    int jpg_count = 0;
    char filename[8];
    FILE *img = NULL;
    while (fread(Buffer, 1, BLOCK_SIZE, card) == BLOCK_SIZE)
    {
        if (Buffer[0] == 0xff && Buffer[1] == 0xd8 && Buffer[2] == 0xff &&
            (Buffer[3] & 0xf0) == 0xe0)
        {
            if (img != NULL)
            {
                fclose(img);
            }
            sprintf(filename, "%03i.jpg", jpg_count);
            img = fopen(filename, "w");
            jpg_count++;
        }
        if (img != NULL)
        {
            fwrite(Buffer, BLOCK_SIZE, 1, img);
        }
    }
    if (img != NULL)
    {
        fclose(img);
    }
    fclose(card);
}
