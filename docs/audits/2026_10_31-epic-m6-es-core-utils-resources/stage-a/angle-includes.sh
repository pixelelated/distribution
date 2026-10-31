#!/bin/bash
# T36 stage A: the 241 angle includes under the lane's own standard list (the brief's § 5 r16 asks for it beside the count).
# STD is the C++17 standard library headers and the C headers they carry, plus the POSIX/Linux system headers by their
# directories (sys/, unistd.h, ...): everything else is non-standard (SDL, GL, FreeType, pugixml, vlc, fribidi, the tree's own).
W=/home/max/Development/emulationstation-next.worktrees/m6-es-core-utils-resources-683; PIN=16dbac5211eea7e70db7394372033be2be7df829
STD='algorithm|array|atomic|bitset|cassert|cctype|cerrno|cfloat|chrono|cinttypes|climits|clocale|cmath|codecvt|condition_variable|cstdarg|cstddef|cstdint|cstdio|cstdlib|cstring|ctime|cwchar|cwctype|deque|exception|fstream|functional|future|iomanip|ios|iosfwd|iostream|istream|iterator|limits|list|locale|map|memory|mutex|new|numeric|ostream|queue|random|ratio|regex|set|shared_mutex|sstream|stack|stdexcept|streambuf|string|string_view|system_error|thread|tuple|type_traits|typeinfo|unordered_map|unordered_set|utility|valarray|vector|assert\.h|ctype\.h|errno\.h|float\.h|inttypes\.h|limits\.h|locale\.h|math\.h|stdarg\.h|stddef\.h|stdint\.h|stdio\.h|stdlib\.h|string\.h|time\.h|wchar\.h|wctype\.h|signal\.h|setjmp\.h|optional|variant|any|filesystem|dirent\.h|fcntl\.h|unistd\.h|pwd\.h|grp\.h|utime\.h|netdb\.h|ifaddrs\.h|termios\.h|dlfcn\.h|pthread\.h|semaphore\.h|sched\.h|libgen\.h|poll\.h|sys/[a-z_]+\.h|net/[a-z_]+\.h|netinet/[a-z_]+\.h|arpa/[a-z_]+\.h|linux/[a-z_]+\.h|strings\.h|alloca\.h|malloc\.h|memory\.h|cstdbool|ciso646|climits|initializer_list|langinfo\.h'
echo "the standard list (regex): $STD"
git -C "$W" grep -h -E '^\s*#\s*include\s*<' "$PIN" -- $(cat .qa-scratch/t36/paths.txt) | sed -E 's/^\s*#\s*include\s*<([^>]+)>.*/\1/' > /workspace/tmp/m6-t36/angle.txt
echo "angle include lines: $(/usr/bin/grep -c '' /workspace/tmp/m6-t36/angle.txt)"
echo "standard by the list: $(/usr/bin/grep -c -x -E "$STD" /workspace/tmp/m6-t36/angle.txt)"
echo "NON-STD ANGLE INCLUDES (lane's list): $(/usr/bin/grep -c -v -x -E "$STD" /workspace/tmp/m6-t36/angle.txt)"
/usr/bin/grep -v -x -E "$STD" /workspace/tmp/m6-t36/angle.txt | sort | uniq -c | sort -rn
