#include "classes/MyClass.h"

#include <gtest/gtest.h>

using ::testing::Eq;

class MyClassTest : public ::testing::Test
{
};

TEST_F(MyClassTest, DoSomething)
{
    MyClass myClass;
    EXPECT_TRUE(myClass.doSomething("Test message"));
}

TEST_F(MyClassTest, HelperFunction)
{
    MyClass myClass;
    // Accessing the private member function via the TV macro
    EXPECT_TRUE(myClass.helperFunction("Test info"));
}