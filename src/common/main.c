#include <stdio.h>

int yyparse (void);

int main()
{
  yyparse();
  printf("Okay!\n");
  return 0;
}
