#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool only_digit(string s);
char rotate(int key, char s);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key \n");
        return 1;
    }
    if (only_digit(argv[1]) == false)
    {
        printf("Usage: ./caesar key \n");
        return 1;
    }
    int key = atoi(argv[1]);
    string Plaintext = get_string("plaintext:  ");
    printf("ciphertext:  ");
    for (int i = 0, len = strlen(Plaintext); i < len; i++)
    {
        if (isalpha(Plaintext[i]))
        {
            printf("%c", rotate(key, Plaintext[i]));
        }
        else
        {
            printf("%c", Plaintext[i]);
        }
    }
    printf("\n");
}
bool only_digit(string s)
{
    for (int i = 0, len = strlen(s); i < len; i++)
    {
        if (!isdigit(s[i]))
        {
            return false;
        }
    }
    return true;
}
char rotate(int key, char s)
{
    int pi;
    int ci;
    if (isupper(s))
    {
        pi = s - 'A';
        ci = (pi + key) % 26;
        return ((char) ci + 'A');
    }
    else if (islower(s))
    {
        pi = s - 'a';
        ci = (pi + key) % 26;
        return ((char) ci + 'a');
    }
    else
    {
        return 0;
    }
}
