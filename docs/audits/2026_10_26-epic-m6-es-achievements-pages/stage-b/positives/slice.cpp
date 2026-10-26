// The rethrow shapes at RetroAchievements.cpp:923-926 and ThreadedHasher.cpp:109-118,
// and the caller's catch at ThreadedHasher.cpp:394-400, at 16dbac5211.
#include <iostream>
#include <stdexcept>
#include <string>
static void getCheevosHashes() {
	try { throw std::domain_error("Error while accessing retroachievements official games list :\nCould not resolve host"); }
	catch (const std::exception& e) { throw e; }   // RetroAchievements.cpp:923-926
	catch (...) {}
}
static void ctor() {
	try { getCheevosHashes(); }
	catch (const std::exception& e) { throw e; }   // ThreadedHasher.cpp:109-118
}
int main() {
	try { ctor(); }
	catch (const std::exception& e) { std::cout << "GuiMsgBox text: [" << e.what() << "]\n"; }   // :396, :399
}
