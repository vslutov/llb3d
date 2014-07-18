#include "helpers/symbol_table.h"

char *char_buffer;
size_t char_buffer_size = 20 * 1000;

Symbol *hashtable;
size_t hashtable_size = 1000;

void 
init_symbol_table (void) 
{
	char_buffer = (char *) malloc ( char_buffer_size );
	hashtable = (Symbol *) malloc ( hashtable_size * sizeof(Symbol) );
}

Symbol *
search_symbol (char *string, size_t length)
{

}

void
register_symbol (char *string, size_t length, Symbol_type symbol_enum);