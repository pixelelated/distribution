#include <iostream>
#include <string>
namespace Utils{namespace String{static std::string trim(const std::string& s){size_t a=s.find_first_not_of(" \t"),b=s.find_last_not_of(" \t");return a==std::string::npos?"":s.substr(a,b-a+1);}}}
int main(){
// ---- verbatim, OfflineScanJob.cpp:196-205 at 16dbac5211 ----
	auto num = [](const std::string& s) -> int
	{
		const std::string t = Utils::String::trim(s);
		if (t.empty() || t.size() > 9)
			return 0;
		for (char c : t)
			if (c < '0' || c > '9')
				return 0;
		return std::stoi(t);
	};
// ----
for (auto s : {"3","unknown",""}) std::cout << "num(\"" << s << "\") = " << num(s) << "\n";
std::cout << "State.ready initial -1 (OfflineScanJob.h:40); after \">>> done 3|0|unknown|0\": " << num("unknown") << "\n"; }
