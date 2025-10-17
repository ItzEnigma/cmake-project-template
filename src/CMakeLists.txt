add_library(${LIB_NAME} STATIC lib/Lib.cpp functions/Functions.cpp)
target_include_directories(${LIB_NAME} PUBLIC inc)
target_link_libraries(${LIB_NAME} PRIVATE fmt::fmt nlohmann_json::nlohmann_json)