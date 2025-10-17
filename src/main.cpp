#include <iostream>

#include "classes/MyClass.h"
#include "functions/Functions.h"
#include "lib/Lib.h"

int main()
{
    json_print();
    libFunction();
    MyClass myClass;
    myClass.doSomething("Hello, from CMake Project!");
    return 0;
}