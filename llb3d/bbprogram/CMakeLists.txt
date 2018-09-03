cmake_minimum_required(VERSION 3.9.2)
project(bbruntime LANGUAGES C ASM)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -std=c99 -Wall -Werror")

file(GLOB PROJECT_SOURCES *.c)

add_executable(bbprogram bbprogram.s)

add_library(libbbruntime_static STATIC IMPORTED)
SET_PROPERTY(TARGET libbbruntime_static PROPERTY IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/libbbruntime_static.a")

find_package(ICU 55.1 COMPONENTS io uc REQUIRED)

target_link_libraries(bbprogram libbbruntime_static ${ICU_LIBRARIES})
