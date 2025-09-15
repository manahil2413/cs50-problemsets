#include <cs50.h>
#include <stdio.h>

void print_bricks(int row);

int main(void)
{
    // user input for height
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1);
    for (int row = 0; row < n; row++)
    {
        for (int col = 0; col < n - (row + 1); col++)
        {
            printf(" ");
        }
        print_bricks(row + 1);
        printf("  ");
        for (int col = 0; col < row + 1; col++)
        {
            printf("#");
        }

        printf("\n");
    }
}
void print_bricks(int row)
{
    for (int brick = 0; brick < row; brick++)
    {
        printf("#");
    }
}
