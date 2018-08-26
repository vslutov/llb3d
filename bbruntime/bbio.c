#include "bbio.h"

#include <stdio.h>

void
Print(char *str) {
  puts(str);
}

void
Write(char *str) {
  fputs(str, stdout);
}
