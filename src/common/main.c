#include "parser.h"

#include <stdio.h>

int main()
{
  yyparse();
  printf("Okay!\n");
  return 0;
}
