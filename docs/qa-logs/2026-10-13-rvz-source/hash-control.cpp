// SPDX-License-Identifier: MIT
// UNRUN: links the exact candidate libcheevos wrapper, without ES UI/accounts.
#include "cheevos.h"
#include <cstdio>
#include <cstring>

int main(int argc, char** argv)
{
    if (argc < 3 || argc % 2 != 1 || argc > 65)
        return 64;
    for (int i = 1; i < argc; i += 2)
    {
        const int console = std::strcmp(argv[i], "gamecube") == 0 ? RC_CONSOLE_GAMECUBE :
            std::strcmp(argv[i], "nes") == 0 ? RC_CONSOLE_NINTENDO : 0;
        if (!console)
            return 64;
        char hash[33] = {};
        if (!generateHashFromFile(hash, console, argv[i + 1]))
        {
            std::puts("FAIL");
            return 2;
        }
        std::puts(hash);
    }
    return 0;
}
