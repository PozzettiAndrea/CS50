#include <cs50.h>
#include <stdio.h>

void dash(int n)
{ for (int i = 0; i < n; i++)
    {printf("#");
    }
}    
void space(int n)
{ for (int i = 0; i < n; i++)
    {printf(" ");
    }
}    
int main(void)
    
{
    int x;
    int x2;
    int line;
      do
          {
          x = get_int("Height: \n");
          }
   while (x < 1 || x > 8);
        x2 = x;
        line = 1;
    while (x2>0)
        {
            space(x-line);
            dash(line-1);
            printf("#  #");
            dash(line-1);
            printf("\n");
         x2 = x2-1;
         line = line + 1;
        }     

}
