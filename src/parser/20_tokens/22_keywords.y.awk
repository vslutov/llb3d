#! /bin/awk -f

{
	print "%token KEYWORD_" $0
}
