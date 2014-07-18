#include <stdio.h>

extern int yylineno;

void yyerror(const char *s) {
	fprintf (stderr, "%s at line %d\n", s, yylineno);
	exit(1);
}
