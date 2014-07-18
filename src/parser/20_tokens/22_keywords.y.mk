$(PARSER_BUILD_DIR)/20_tokens/22_keywords.y : $(PARSER_SOURCE_DIR)/20_tokens/22_keywords.y.awk
	mkdir -p $(PARSER_BUILD_DIR)/20_tokens
	awk -f $(PARSER_SOURCE_DIR)/20_tokens/22_keywords.y.awk < $(COMMON_SOURCE_DIR)/keywords.list > $(PARSER_BUILD_DIR)/20_tokens/22_keywords.y

PARSER_BUILD_FILES := $(PARSER_BUILD_FILES) $(PARSER_BUILD_DIR)/20_tokens/22_keywords.y
