#include <gtest/gtest.h>
#include <gmock/gmock.h>

#include <nlohmann/json.hpp>

using json = nlohmann::json;
using ::testing::Eq;

class JsonTest : public ::testing::Test
{
protected:
    json j;

    void SetUp() override
    {
        j["name"] = "John";
        j["age"] = 30;
        j["city"] = "New York";
    }
};

TEST(JsonTest2, BasicJson)
{
    // Create a JSON object
    json j;
    j["name"] = "John";
    j["age"] = 30;
    j["city"] = "New York";

    // Check if the JSON object contains the expected values
    EXPECT_EQ(j["name"], "John");
    EXPECT_EQ(j["age"], 30);
    EXPECT_EQ(j["city"], "New York");

    // Check if the JSON object has the correct number of elements
    EXPECT_EQ(j.size(), 3);

    // Check if a key exists in the JSON object
    EXPECT_TRUE(j.contains("name"));
    EXPECT_FALSE(j.contains("country"));
}

TEST_F(JsonTest, ModifyJson)
{
    // Modify the JSON object
    j["age"] = 31;
    j["country"] = "USA";

    // Check if the modifications are correct
    EXPECT_EQ(j["age"], 31);
    EXPECT_EQ(j["country"], "USA");
    EXPECT_EQ(j.size(), 4);
}