cmake_minimum_required(VERSION 3.7)
project(bbruntime LANGUAGES C)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -std=c99 -Wall -Werror")

file(GLOB PROJECT_SOURCES *.c)

find_package(ICU 52.1 COMPONENTS io uc REQUIRED)
include_directories(${ICU_INCLUDE_DIRS})

add_library(bbruntime_static STATIC ${PROJECT_SOURCES})
add_library(bbruntime_shared SHARED ${PROJECT_SOURCES})
