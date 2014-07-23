BUILD_DIR  = build
SOURCE_DIR = src
TEST_DIR   = test

CFLAGS = -O2 -Wall -Werror -Wformat-security -Wignored-qualifiers -Winit-self -Wswitch-default -Wfloat-equal -Wpointer-arith -Wtype-limits -Wempty-body -Wno-logical-op -Wstrict-prototypes -Wold-style-declaration -Wold-style-definition -Wmissing-parameter-type -Wmissing-field-initializers -Wnested-externs -Wno-pointer-sign

EXECUTABLE = $(BUILD_DIR)/b3d.exe

.SILENT : all
all : $(EXECUTABLE) test
	touch all

AVAILABLE_BUILDS = all

.SILENT : help
.PHONY : help
help :
	echo "This Makefile contains several targets:"
	echo "  all [default] - build a project"
	echo "  clean         - remove temporary files"
	echo "	test          - make build test [only for debugging]"

clean :
	rm -rf $(BUILD_DIR) $(AVAILABLE_BUILDS)

# Tests

.PHONY : test
.SILENT : test
test : $(EXECUTABLE)
	echo $(shell $(EXECUTABLE) < $(TEST_DIR)/example.bb)

# Build dir

build :
	mkdir -p $(BUILD_DIR)

# Common source

COMMON_SOURCE_DIR   = $(SOURCE_DIR)/common
COMMON_SOURCE_FILES = $(wildcard $(COMMON_SOURCE_DIR)/*.c)

HEADERS_SCRIPT = $(BUILD_DIR)/headers_script.mk
$(HEADERS_SCRIPT) : $(BUILD_DIR)
	echo headers.h | awk -f build_script.awk > $(HEADERS_SCRIPT)
include $(HEADERS_SCRIPT)

# Lexer

LEXER_L = $(BUILD_DIR)/lexer.l

LEXER_C = $(BUILD_DIR)/lexer.c
GENERATED_SOURCE_FILES := $(GENERATED_SOURCE_FILES) $(LEXER_C)

LEXER_H = $(BUILD_DIR)/lexer.h
HEADERS_BUILD_FILES := $(HEADERS_BUILD_FILES) $(LEXER_H)

LEXER_SCRIPT = $(BUILD_DIR)/lexer_script.mk
$(LEXER_SCRIPT) : $(BUILD_DIR)
	echo lexer.l | awk -f build_script.awk > $(LEXER_SCRIPT)
include $(LEXER_SCRIPT)

$(LEXER_L) : $(LEXER_BUILD_FILES)
	cat $(LEXER_BUILD_SORTED_FILES) > $(LEXER_L)

$(LEXER_C) $(LEXER_H) : $(LEXER_L) $(BUILD_DIR)
	lex --nounistd -i --outfile=$(LEXER_C) --header-file=$(LEXER_H) $(LEXER_L)

# Parser

PARSER_Y = $(BUILD_DIR)/parser.y

PARSER_C = $(BUILD_DIR)/parser.c
GENERATED_SOURCE_FILES := $(GENERATED_SOURCE_FILES) $(PARSER_C)

PARSER_H = $(HEADERS_BUILD_DIR)/parser.h
HEADERS_BUILD_FILES := $(HEADERS_BUILD_FILES) $(PARSER_H)

PARSER_SCRIPT = $(BUILD_DIR)/parser_script.mk
$(PARSER_SCRIPT) : $(BUILD_DIR)
	echo parser.y | awk -f build_script.awk > $(PARSER_SCRIPT)
include $(PARSER_SCRIPT)

$(PARSER_Y) : $(PARSER_BUILD_FILES)
	cat $(PARSER_BUILD_SORTED_FILES) > $(PARSER_Y)

$(PARSER_C) $(PARSER_H) : $(PARSER_Y) $(BUILD_DIR) $(HEADERS_BUILD_DIR)
	bison --output=$(PARSER_C) --defines=$(PARSER_H) $(PARSER_Y)

# Binary files

COMMON_BINARY_DIR   = $(BUILD_DIR)/common
COMMON_BINARY_FILES = $(patsubst $(COMMON_SOURCE_DIR)/%.c, $(COMMON_BINARY_DIR)/%.o, $(COMMON_SOURCE_FILES))

$(COMMON_BINARY_DIR) : $(BUILD_DIR)
	mkdir -p $(COMMON_BINARY_DIR)

$(COMMON_BINARY_FILES) : $(COMMON_BINARY_DIR)/%.o : $(COMMON_SOURCE_DIR)/%.c $(HEADERS_BUILD_FILES) $(COMMON_BINARY_DIR)
	tcc $(CFLAGS) -I$(HEADERS_BUILD_DIR) -c -o $@ $<

GENERATED_BINARY_FILES = $(GENERATED_SOURCE_FILES:.c=.o)
$(GENERATED_BINARY_FILES) : $(BUILD_DIR)/%.o : $(BUILD_DIR)/%.c
	tcc $(CFLAGS) -I$(HEADERS_BUILD_DIR) -c -o $@ $<

BINARY_FILES = $(COMMON_BINARY_FILES) $(GENERATED_BINARY_FILES)

# Executable

$(EXECUTABLE) : $(BINARY_FILES)
	gcc -o $(EXECUTABLE) $(BINARY_FILES)

