$(LEXER_BUILD_DIR)/40_rules/47_keywords.l : $(LEXER_SOURCE_DIR)/40_rules/47_keywords.l.awk
	mkdir -p $(LEXER_BUILD_DIR)/40_rules/
	awk -f $(LEXER_SOURCE_DIR)/40_rules/47_keywords.l.awk < $(COMMON_SOURCE_DIR)/keywords.list > $(LEXER_BUILD_DIR)/40_rules/47_keywords.l

LEXER_BUILD_FILES := $(LEXER_BUILD_FILES) $(LEXER_BUILD_DIR)/40_rules/47_keywords.l
