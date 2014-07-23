#!/usr/bin/nawk -f

{
	if (match($0, "^[^.]+.")) {
		PREFIX     = toupper( substr($0, RSTART, RLENGTH - 1) )
		foldername = tolower(PREFIX)
		ext        = substr($0, 1 + RLENGTH)
		SUFFIX     = toupper(ext)

		print PREFIX "_SOURCE_DIR = $(SOURCE_DIR)/" foldername
		print PREFIX "_BUILD_DIR  = $(BUILD_DIR)/" foldername

		print "$(" PREFIX "_BUILD_DIR) : $(BUILD_DIR)"
		print "		mkdir -p $(" PREFIX "_BUILD_DIR)"


		print PREFIX "_SOURCE_FOLDERS = $(wildcard $(" PREFIX "_SOURCE_DIR)/*/)"
		print PREFIX "_BUILD_FOLDERS  = $(subst    $(" PREFIX "_SOURCE_DIR)/, $(" PREFIX "_BUILD_DIR)/, $(" PREFIX "_SOURCE_FOLDERS))"

		print "$(" PREFIX "_BUILD_FOLDERS) : $(" PREFIX "_BUILD_DIR)/% : $(" PREFIX "_BUILD_DIR)"
		print "		mkdir -p $@"


		print PREFIX "_SOURCE_FILES_" SUFFIX " = $(wildcard $(" PREFIX "_SOURCE_DIR)/*/*." ext ")"
		print PREFIX "_BUILD_FILES_" SUFFIX "  = $(patsubst $(" PREFIX "_SOURCE_DIR)/%." ext ", $(" PREFIX "_BUILD_DIR)/%." ext ", $(" PREFIX "_SOURCE_FILES_" SUFFIX "))"

		print "$(" PREFIX "_BUILD_FILES_" SUFFIX ") : $(" PREFIX "_BUILD_DIR)/%." ext " : $(" PREFIX "_SOURCE_DIR)/%." ext " $(" PREFIX "_BUILD_FOLDERS)"
		print "		cp $< $@"


		print PREFIX "_BUILD_FILES        := $(" PREFIX "_BUILD_FILES_" SUFFIX ")"
		print PREFIX "_BUILD_SORTED_FILES =  $(sort $(" PREFIX "_BUILD_FILES))"

		print PREFIX "_MAKEFILES = $(wildcard $(" PREFIX "_SOURCE_DIR)/*/*.mk)"
		print "include $(" PREFIX "_MAKEFILES)"
	}
}


