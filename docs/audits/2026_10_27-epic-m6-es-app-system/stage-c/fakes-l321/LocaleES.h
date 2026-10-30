// T33 S3 fake (#680): `_()` returns its msgid, as an untranslated build does.
#pragma once
#include <string>
#define _(x) std::string(x)
