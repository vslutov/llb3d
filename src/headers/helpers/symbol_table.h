#ifndef SYMBOL_TABLE_H
#define SYMBOL_TABLE_H

#include <stdlib.h>

typedef enum
{
	SYMBOL_LOCAL,
	SYMBOL_GLOBAL,
	SYMBOL_FUNCTION,
	SYMBOL_TYPE
} Symbol_type;

typedef struct
{
	char *string;
	size_t hash;
} Symbol;

void 
init_symbol_table (void);

Symbol *
search_symbol (char *string, size_t length);

void
register_symbol (char *string, size_t length, Symbol_type symbol_enum);

#endif
