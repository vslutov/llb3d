cmake_minimum_required(VERSION 3.9.2)
project(bbruntime LANGUAGES C ASM)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -std=c99 -Wall -Werror")

file(GLOB PROJECT_SOURCES *.c)

add_executable(bbprogram bbprogram.s)

add_library(libbbruntime STATIC IMPORTED)
SET_PROPERTY(TARGET libbbruntime PROPERTY IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/libbbruntime.a")

target_link_libraries(bbprogram libbbruntime)
