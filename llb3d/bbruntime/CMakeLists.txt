cmake_minimum_required(VERSION 3.9.2)
project(bbruntime LANGUAGES C)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -std=c99 -Wall -Werror")

file(GLOB PROJECT_SOURCES *.c)

find_package(ICU 55.1 COMPONENTS io uc REQUIRED)
include_directories(${ICU_INCLUDE_DIRS})

add_library(bbruntime_static STATIC ${PROJECT_SOURCES})
add_library(bbruntime_shared SHARED ${PROJECT_SOURCES})
