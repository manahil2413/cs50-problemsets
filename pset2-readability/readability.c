#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int count_letters(string text,int len);
int count_words(string text, int len);
int count_sentences(string text , int len);


int main(void)
{
  string text = get_string("Text:  ");
  const int length = strlen(text);
  int letters = count_letters(text,length);
  int words = count_words(text,length);
  int sentences = count_sentences(text,length);
  double L = (letters/(float)words)*100;
  double s = (sentences/(float)words)*100;
  double i = 0.0588*L -0.296*s - 15.8;
  int index = round(i);

  if (index < 1)
  {
    printf("Before Grade 1\n");
  }

  else if (index > 16)
  {
    printf("Grade 16+\n");
  }
  else
  {
    printf("Grade %i\n",index);
  }


}




int count_letters(string text, int len)
{
    int n = 0;
    for (int i = 0; i < len; i++ )
    {
        if(isalpha(text[i]))
        {
          n++;
        }
    }
    return n;
}
int count_words(string text, int len)
{
   int space = 0;
   for (int i = 0 ; i < len; i++)
   {
    if(isblank(text[i]))
    {
        space++;
    }
   }
   return space+1;
}
int count_sentences(string text , int len)
{
   int n = 0;
   for (int i = 0; i < len; i++)
   {
    if (text[i]=='.' || text[i]=='?' || text[i] == '!')
    {
        n++;
    }
   }
   return n;
}

