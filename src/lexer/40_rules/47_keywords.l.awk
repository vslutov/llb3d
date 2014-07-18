#! /bin/awk -f

{
	print $0 " { return KEYWORD_" $0 "; }"
}
