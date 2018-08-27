cmake_minimum_required(VERSION 3.11.2)
project(bbruntime LANGUAGES C)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -std=c99 -Wall -Werror")

file(GLOB PROJECT_SOURCES *.c)

add_library(bbruntime STATIC ${PROJECT_SOURCES})
