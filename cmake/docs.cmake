find_package(Doxygen)

if(DOXYGEN_FOUND)
    add_custom_target(docs
        COMMAND ${DOXYGEN_EXECUTABLE}
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/docs
        COMMENT "Generating HTML documentation with Doxygen"
    )
else()
    message(WARNING "Doxygen not found, documentation will not be generated.")
endif()