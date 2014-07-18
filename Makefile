BUILD_DIR  = build
SOURCE_DIR = src
TEST_DIR   = test

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
	mkdir $(BUILD_DIR)

# Common source

COMMON_SOURCE_DIR    = $(SOURCE_DIR)/common
COMMON_SOURCE_FILES := $(COMMON_SOURCE_DIR)/*.c

HEADERS_SCRIPT = $(BUILD_DIR)/headers_script.mk
$(HEADERS_SCRIPT) : $(BUILD_DIR)
	echo headers.h | awk -f build_script.awk > $(HEADERS_SCRIPT)
include $(HEADERS_SCRIPT)

# Lexer

LEXER_L = $(BUILD_DIR)/lexer.l

LEXER_C = $(BUILD_DIR)/lexer.c
COMMON_SOURCE_FILES := $(COMMON_SOURCE_FILES) $(LEXER_C)

LEXER_SCRIPT = $(BUILD_DIR)/lexer_script.mk
$(LEXER_SCRIPT) : $(BUILD_DIR)
	echo lexer.l | awk -f build_script.awk > $(LEXER_SCRIPT)
include $(LEXER_SCRIPT)

$(LEXER_L) : $(LEXER_BUILD_FILES)
	cat $(LEXER_BUILD_SORTED_FILES) > $(LEXER_L)

$(LEXER_C) : $(LEXER_L)
	lex --nounistd -t -i $(LEXER_L) > $(LEXER_C)

# Parser

PARSER_Y = $(BUILD_DIR)/parser.y

PARSER_C = $(BUILD_DIR)/parser.c
COMMON_SOURCE_FILES := $(COMMON_SOURCE_FILES) $(PARSER_C)

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

# Executable

$(EXECUTABLE) : $(COMMON_SOURCE_FILES) $(HEADERS_BUILD_FILES) $(BUILD_DIR)
	tcc -I$(HEADERS_BUILD_DIR) $(COMMON_SOURCE_FILES) -o $(EXECUTABLE)
