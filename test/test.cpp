#include "gmock/gmock.h"
#include "gtest/gtest.h"

TEST(SampleTest, BasicAssertions)
{
    // Expect two strings to be equal.
    EXPECT_STREQ("hello", "hello");

    // Expect two integers to be equal.
    EXPECT_EQ(42, 42);

    // Expect a condition to be true.
    EXPECT_TRUE(1 + 1 == 2);
}