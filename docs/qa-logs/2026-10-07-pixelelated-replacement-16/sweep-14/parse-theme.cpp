// Read the actual theme dialect with the exact consumed pugixml source.
// ThemeData.cpp uses load_file with default flags. Serialization escapes
// literal && conditions for strict XML analysis; source/artifact stay intact.
#include "pugixml.hpp"
#include <cstdio>
int main(int argc,char**argv) {
    if (argc != 3) return 2;
    pugi::xml_document doc;
    auto result=doc.load_file(argv[1]);
    if (!result) { std::fprintf(stderr,"theme parse failed: %s\n",result.description()); return 1; }
    if (!doc.child("theme")) return 1;
    if (!doc.save_file(argv[2])) return 1;
    std::puts("PASS actual pugixml default-load theme parser");
    return 0;
}
