#include "bbio.h"
#include "bbglobals.h"

#include <unicode/ustdio.h>

void
Print(const UChar *str) {
  Write(str);
  u_fputc('\n', ustdout);
}

void
Write(const UChar *str) {
  u_file_write(str, u_strlen(str), ustdout);
}
