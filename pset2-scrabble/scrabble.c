#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int calculate_score(string s);
int Points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int main(void)
{
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");
    int Point1 = calculate_score(word1);
    int Point2 = calculate_score(word2);
    if (Point1 > Point2)
    {
        printf("Player 1 wins!\n");
    }
    else if (Point2 > Point1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int calculate_score(string s)
{
    int score = 0;
    for (int i = 0, len = strlen(s); i < len; i++)
    {
        if (isupper(s[i]))
        {
            score += Points[s[i] - 'A'];
        }
        else if (islower(s[i]))
        {
            score += Points[s[i] - 'a'];
        }
    }
    return score;
}
