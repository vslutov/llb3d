$(PARSER_BUILD_DIR)/40_rules/43_dynamic_operators.y : $(PARSER_SOURCE_DIR)/40_rules/43_dynamic_operators.y.c
	mkdir -p $(PARSER_BUILD_DIR)/40_rules
	tcc -run $(PARSER_SOURCE_DIR)/40_rules/43_dynamic_operators.y.c > $(PARSER_BUILD_DIR)/40_rules/43_dynamic_operators.y

PARSER_BUILD_FILES := $(PARSER_BUILD_FILES) $(PARSER_BUILD_DIR)/40_rules/43_dynamic_operators.y
