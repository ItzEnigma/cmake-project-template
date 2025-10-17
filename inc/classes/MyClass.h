#pragma once

#include <string>

#include "util/Testing.h"

class MyClass
{
public:
    MyClass();
    ~MyClass();

    bool doSomething(std::string message);

    TV(private):
	bool helperFunction(std::string info);
};