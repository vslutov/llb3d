{number}		{ yylval->integer_val = atoi(yytext);
              return INTEGER_VALUE; }
