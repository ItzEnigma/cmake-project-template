#include "classes/MyClass.h"

#include <fmt/core.h>
#include <nlohmann/json.hpp>

#include <iostream>

MyClass::MyClass() {}

MyClass::~MyClass() {}

bool MyClass::doSomething(std::string message)
{
    fmt::print("Doing something with message: {}\n", message);
    return helperFunction(message);
}

bool MyClass::helperFunction(std::string info)
{
    if (info.empty())
    {
        fmt::print("Helper function received empty info.\n");
        return false;
    }
    fmt::print("Helper function called with info: {}\n", info);
    return true;
}