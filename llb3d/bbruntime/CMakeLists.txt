cmake_minimum_required(VERSION 3.7)
project(bbruntime LANGUAGES C)

set(ICU_C_FLAGS "-DU_STATIC_IMPLEMENTATION -DUCONFIG_ONLY_COLLATION=1 -DUCONFIG_NO_LEGACY_CONVERSION=1 -DUCONFIG_NO_COLLATION=1")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -std=c99 -Wall -Werror ${ICU_C_FLAGS}")

file(GLOB PROJECT_SOURCES *.c)
file(GLOB ICU_STATIC_LIBRARIES "/opt/icu/lib/libicu*.a")

include_directories("/opt/icu/include/")

add_library(bbruntime STATIC ${PROJECT_SOURCES})
add_custom_command(TARGET bbruntime
                   POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy ${ICU_STATIC_LIBRARIES} ${CMAKE_ARCHIVE_OUTPUT_DIRECTORY})
