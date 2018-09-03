#include "bbstart.h"
#include "bbglobals.h"

#include <stdio.h>

#include <unicode/uclean.h>
#include <unicode/utypes.h>
#include <unicode/ustdio.h>

int32_t
bbinit(void)
{
  UErrorCode error = U_ZERO_ERROR;
  u_init(&error);
  if (U_FAILURE(error)) {
    printf("ICU init error: %d", error);
    return error;
  }

  ustdin = u_fadopt(stdin, NULL, NULL);
  ustdout = u_get_stdout();
  ustderr = u_fadopt(stderr, NULL, NULL);

  return 0;
}

int
main(void)
{
  int32_t error = bbinit();
  if (error != 0) {
    return error;
  }

  bbmain();

  return 0;
}
