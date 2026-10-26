#include <fstream>
#include <sstream>
#include <string>
#include <iostream>
#define WINSTRINGW(x) x
		static void skipUtf8Bom(std::ifstream& file) 
		{
			if (!file.is_open())
				return;

			char bom[3];
			if (file.read(bom, 3) && bom[0] == '\xEF' && bom[1] == '\xBB' && bom[2] == '\xBF')			
				return;
			
			file.seekg(0);
		}
		std::string	readAllText(const std::string& fileName)
		{
			std::ifstream t(WINSTRINGW(fileName));

			skipUtf8Bom(t);

			std::stringstream buffer;
			buffer << t.rdbuf();
			return buffer.str();
		}
int main(int c, char** v){ for (int i = 1; i < c; i++) std::cout << v[i] << " -> [" << readAllText(v[i]) << "]\n"; }
