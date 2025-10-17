#pragma once

#ifdef UNIT_TESTING
    #define TV(visibility) public
#else
    #define TV(visibility) visibility
#endif