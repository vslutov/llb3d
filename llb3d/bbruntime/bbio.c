#include "bbio.h"
#include "bbglobals.h"

#include <unicode/ustdio.h>

void
Print(UChar *str) {
  Write(str);
  u_fputc('\n', ustdout);
}

void
Write(UChar *str) {
  u_file_write(str, u_strlen(str), ustdout);
}
