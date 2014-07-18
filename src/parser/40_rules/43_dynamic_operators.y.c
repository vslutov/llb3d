#include <stdio.h>
#include <stdlib.h>

#define COUNT_OF_LEVELS 11
#define MAX_OPERATORS_IN_LEVEL 7

typedef char * String;

typedef enum {
	Unary,
	Binary
} Arity;

typedef struct {
	String name;
	Arity arity;
	String operator_tokens[MAX_OPERATORS_IN_LEVEL + 1];
} OperatorLevel;

OperatorLevel levels[COUNT_OF_LEVELS] =
{
	{
		"UNARY_CUSTOM_TYPE",
		Unary,
		{
			"KEYWORD_NEW",
			"KEYWORD_FIRST",
			"KEYWORD_LAST",
			NULL
		}
	},
	{
		"UNARY_OBJECT",
		Unary,
		{	
			"KEYWORD_BEFORE",
			"KEYWORD_AFTER",
			NULL
		}
	},
	{
		"UNARY_TYPE_CONVERSION",
		Unary,
		{
			"KEYWORD_INT",
			"KEYWORD_FLOAT",
			"KEYWORD_STR",
			NULL
		}
	},
	{
		"UNARY_OTHER",
		Unary,
		{
			"TOKEN_PLUS",
			"TOKEN_MINUS",
			"TOKEN_TILDA",
			NULL
		}
	},
	{
		"BINARY_TO_THE_POWER_OF",
		Binary,
		{
			"TOKEN_CARET",
			NULL
		}
	},
	{
		"BINARY_MULTIPLICATIVE",
		Binary,
		{
			"TOKEN_MULTIPLY",
			"TOKEN_DIVIDE",
			"KEYWORD_MOD",
			NULL
		}
	},
	{
		"BINARY_BITWISE_SHIFT",
		Binary,
		{
			"KEYWORD_SHL",
			"KEYWORD_SHR",
			"KEYWORD_SAR",
			NULL
		}
	},
	{
		"BINARY_ADDITIVE",
		Binary,
		{
			"TOKEN_PLUS",
			"TOKEN_MINUS",
			NULL
		}
	},
	{
		"BINARY_COMPARISON",
		Binary,
		{
			"TOKEN_LESS",
			"TOKEN_MORE",
			"TOKEN_LESS_OR_EQUAL",
			"TOKEN_MORE_OR_EQUAL",
			"TOKEN_EQUAL",
			"TOKEN_NOT_EQUAL",
			NULL
		}
	},
	{
		"BINARY_BITWIZE_ARETHMETIC",
		Binary,
		{
			"KEYWORD_AND",
			"KEYWORD_OR",
			"KEYWORD_XOR",
			NULL
		}
	},
	{
		"UNARY_LOGICAL_NOT",
		Binary,
		{
			"KEYWORD_NOT",
			NULL
		}
	}
};

int main (void)
{
	for (size_t i = 1; i < COUNT_OF_LEVELS; ++ i)
		{
			printf("OPERATOR_%s: ", levels[i].name);
			for (size_t j = 0; levels[i].operator_tokens[j] != NULL; ++ j)
				if (levels[i].arity == Unary)
					printf("%s OPERATOR_%s | ", levels[i].operator_tokens[j], levels[i].name);
				else
					printf("OPERATOR_%s %s OPERATOR_%s | ", levels[i].name, levels[i].operator_tokens[j], levels[i-1].name);
			printf("OPERATOR_%s ;\n", levels[i-1].name);
		}
	return 0;
}
