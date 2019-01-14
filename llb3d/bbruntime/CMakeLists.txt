cmake_minimum_required(VERSION 3.7)
project(bbruntime LANGUAGES C)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -std=c99 -Wall -Werror")

file(GLOB PROJECT_SOURCES *.c)
file(GLOB ICU_STATIC_LIBRARIES "/opt/icu/lib/libicu*.a")

include_directories("/opt/icu/include/")

add_library(bbruntime STATIC ${PROJECT_SOURCES})
add_custom_command(TARGET bbruntime
                   POST_BUILD COMMAND ${CMAKE_COMMAND} -E copy ${ICU_STATIC_LIBRARIES} ${CMAKE_ARCHIVE_OUTPUT_DIRECTORY})
