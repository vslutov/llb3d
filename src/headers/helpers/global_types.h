#ifndef GLOBAL_TYPES_H
#define GLOBAL_TYPES_H

typedef const char *String;
typedef struct
{
  size_t length;
  String pointer;
} SizedString;

#endif

