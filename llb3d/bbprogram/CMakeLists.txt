cmake_minimum_required(VERSION 3.9.2)
project(bbprogram LANGUAGES C ASM)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -std=c99 -Wall -Werror")

file(GLOB PROJECT_SOURCES *.c)
file(GLOB STATIC_LIBRARIES *.a)

add_executable(bbprogram bbprogram.s)

# add_library(bbruntime STATIC IMPORTED)
# SET_PROPERTY(TARGET bbruntime PROPERTY IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/libbbruntime.a")
#
# add_library(icuuc STATIC IMPORTED)
# SET_PROPERTY(TARGET icuuc PROPERTY IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/libicuuc.a")
#
# add_library(icuio STATIC IMPORTED)
# SET_PROPERTY(TARGET icuio PROPERTY IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/libicuio.a")
#
# add_library(icudata STATIC IMPORTED)
# SET_PROPERTY(TARGET icudata PROPERTY IMPORTED_LOCATION "${CMAKE_CURRENT_SOURCE_DIR}/libicudata.a")
#
# set(ICU_LIBRARIES icuuc icuio icudata)

target_link_libraries(bbprogram ${STATIC_LIBRARIES})
