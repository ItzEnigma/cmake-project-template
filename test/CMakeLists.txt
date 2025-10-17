include_directories(inc)
set(TEST_EXECUTABLE "test")
file(GLOB_RECURSE TEST_FILES ${CMAKE_CURRENT_LIST_DIR}/*.cpp)
add_executable(${TEST_EXECUTABLE} ${TEST_FILES} ${CMAKE_SOURCE_DIR}/src/classes/MyClass.cpp)
target_link_libraries(${TEST_EXECUTABLE} gtest gmock_main ${LIB_NAME} fmt::fmt nlohmann_json::nlohmann_json)

target_compile_definitions(${TEST_EXECUTABLE} PRIVATE UNIT_TESTING)

include(GoogleTest)
gtest_discover_tests(${TEST_EXECUTABLE})

if(ENABLE_COVERAGE)
    set(COVERAGE_MAIN "coverage")
    set(COVERAGE_EXCLUDES
        "${PROJECT_SOURCE_DIR}/app/*"
        "${PROJECT_SOURCE_DIR}/cmake/*"
        "${PROJECT_SOURCE_DIR}/docs/*"
        "${PROJECT_SOURCE_DIR}/external/*"
        "${PROJECT_SOURCE_DIR}/test/*"
        "${PROJECT_SOURCE_DIR}/build/*"
        "/usr/include/*")
    set(COVERAGE_EXTRA_FLAGS)
    set(COVERAGE_DEPENDENCIES test)

    setup_target_for_coverage_gcovr_html(
        NAME
        ${COVERAGE_MAIN}
        EXECUTABLE
        ${TEST_EXECUTABLE} --gtest_brief=1
        DEPENDENCIES
        ${COVERAGE_DEPENDENCIES}
        BASE_DIRECTORY
        ${CMAKE_SOURCE_DIR})
endif()
