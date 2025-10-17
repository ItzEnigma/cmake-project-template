cmake_minimum_required(VERSION 3.22)

# Project Version --> Major.Minor.Patch
project("CMake Project" VERSION 1.0.0 LANGUAGES C CXX) # CXX for C++ (as + is not valid)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF) # Use -std=c++17, not -std=gnu++17 (without system-specific extensions)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON) # Important for
set(CMAKE_BUILD_PARALLEL_LEVEL 8)

# OPTIONS
option(ENABLE_COVERAGE "Enable a Code Coverage build." OFF)

set(LIB_NAME "Lib")
set(EXECUTABLE_NAME "MyApp")
set(LOG_DIR "${CMAKE_BINARY_DIR}/logs")

# cmake files
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/")
include(dependencies)
include(docs) # Doxygen documentation

if(ENABLE_COVERAGE)
    include(CodeCoverage)
    append_coverage_compiler_flags()
endif()

include(${CMAKE_CURRENT_SOURCE_DIR}/src/CMakeSourceLists.txt) # Include the list of source files

add_executable(${EXECUTABLE_NAME} ${SRC_FILES})
target_link_libraries(${EXECUTABLE_NAME} PRIVATE ${LIB_NAME} fmt::fmt nlohmann_json::nlohmann_json)

add_subdirectory(config) # Configuration files
include_directories(inc)
add_subdirectory(src)
add_subdirectory(test)