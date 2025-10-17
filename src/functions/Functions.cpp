#include "functions/Functions.h"

#include <fmt/core.h>
#include <nlohmann/json.hpp>

void json_print()
{
    nlohmann::json j;
    j["name"] = "Enigma";
    j["age"] = 1020;
    fmt::print("JSON: {}\n", j.dump(2));
}
