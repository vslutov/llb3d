#ifndef SYMBOL_TABLE_H
#define SYMBOL_TABLE_H

#include "helpers/global_types.h"

#include <stdlib.h>

typedef enum
{
  SYMBOL_LOCAL,
  SYMBOL_GLOBAL,
  SYMBOL_FUNCTION,
  SYMBOL_TYPE
} Symbol_type;

typedef struct symbol_struct
{
  Symbol_type type;
  String name;
} *Symbol;

struct node;

typedef struct node **SymbolTable;

Symbol
GetSymbol (String s, SymbolTable root);

#endif

