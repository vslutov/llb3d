#include "bbstart.h"
#include "bbglobals.h"

#include <stdio.h>
#include <stdlib.h>

#include <unicode/uclean.h>
#include <unicode/utypes.h>
#include <unicode/ustdio.h>

void
bbinit(void)
{
  UErrorCode error = U_ZERO_ERROR;
  u_init(&error);
  if (U_FAILURE(error)) {
    printf("ICU init error: %d", error);
    exit(EXIT_FAILURE);
  }

  ustdin = u_fadopt(stdin, NULL, NULL);
  ustdout = u_get_stdout();
  ustderr = u_fadopt(stderr, NULL, NULL);
}

void
bbstart(void)
{
  bbinit();

  bbmain();
}

int
main(void)
{
  bbstart();
  return 0;
}
