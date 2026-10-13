// SPDX-License-Identifier: MIT
// UNRUN: pure eligibility controls, no files, UI, accounts, or network.
#include "GameCubeRvzHashRetry.h"
#include "CheevosIndex.h"
#include <cstdio>
#include <string>

int main()
{
    using CheevosIndex::Take;
    const std::string zero(32, '0'), valid(32, 'a'), upper(32, 'B');
    struct Case
    {
        const char* name;
        bool enabled, gamecube, force;
        std::string extension, hash, id;
        bool retry;
        Take before, after;
    };
    const Case cases[] = {
        {"retained-zero-no-id", true,true,false,".rvz",zero,"",true,Take::Lookup,Take::Hash},
        {"retained-zero-id-marker", true,true,false,".rvz",zero,"0",true,Take::Lookup,Take::Hash},
        {"uppercase-extension", true,true,false,".RVZ",zero,"",true,Take::Lookup,Take::Hash},
        {"invalid-short-hash", true,true,false,".rvz","bad","",true,Take::Lookup,Take::Hash},
        {"invalid-hex-hash", true,true,false,".rvz",std::string(32,'g'),"",true,Take::Lookup,Take::Hash},
        {"missing-hash", true,true,false,".rvz","","",true,Take::Hash,Take::Hash},
        {"whitespace-hash", true,true,false,".rvz"," \t ","",true,Take::Hash,Take::Hash},
        {"trimmed-failure-marker", true,true,false,".rVz"," " + zero + " "," 0 ",true,Take::Lookup,Take::Hash},
        {"valid-unknown", true,true,false,".rvz",valid,"",false,Take::Lookup,Take::Lookup},
        {"valid-unknown-uppercase", true,true,false,".rvz",upper,"0",false,Take::Lookup,Take::Lookup},
        {"valid-hash-whitespace-unchanged", true,true,false,".rvz"," " + valid + " ","",false,Take::Lookup,Take::Lookup},
        {"legitimate-indexed", true,true,false,".rvz",valid,"42",false,Take::None,Take::None},
        {"positive-id-protects-zero", true,true,false,".rvz",zero,"42",false,Take::None,Take::None},
        {"positive-id-protects-invalid", true,true,false,".rvz","bad","0042",false,Take::None,Take::None},
        {"opaque-id-preserved", true,true,false,".rvz",zero,"opaque",false,Take::Lookup,Take::Lookup},
        {"negative-id-preserved", true,true,false,".rvz",zero,"-1",false,Take::Lookup,Take::Lookup},
        {"noncanonical-zero-id-preserved", true,true,false,".rvz",zero,"000",false,Take::Lookup,Take::Lookup},
        {"other-console", true,false,false,".rvz",zero,"",false,Take::Lookup,Take::Lookup},
        {"mixed-platform-not-unambiguous", true,false,false,".rvz",zero,"",false,Take::Lookup,Take::Lookup},
        {"reader-disabled", false,true,false,".rvz",zero,"",false,Take::Lookup,Take::Lookup},
        {"raw-iso-unchanged", true,true,false,".iso",zero,"",false,Take::Lookup,Take::Lookup},
        {"chd-unchanged", true,true,false,".chd",zero,"",false,Take::Lookup,Take::Lookup},
        {"archive-unchanged", true,true,false,".zip",zero,"",false,Take::Lookup,Take::Lookup},
        {"suffix-not-rvz", true,true,false,".rvz.bak",zero,"",false,Take::Lookup,Take::Lookup},
        {"force-all-unchanged", true,true,true,".rvz",valid,"42",false,Take::Hash,Take::Hash},
        {"old-missing-other-format", true,true,false,".iso","","",false,Take::Hash,Take::Hash},
        {"old-missing-with-id", true,true,false,".rvz","","42",false,Take::Hash,Take::Hash},
    };
    int failures = 0;
    for (const auto& item : cases)
    {
        const bool retry = GameCubeRvzHashRetry::needed(item.enabled, item.gamecube,
            item.extension, item.hash, item.id);
        const auto before = CheevosIndex::take(item.force, item.hash, item.id);
        const auto after = retry ? Take::Hash : before;
        const bool passed = retry == item.retry && before == item.before && after == item.after;
        std::printf("%s %s\n", passed ? "PASS" : "FAIL", item.name);
        failures += !passed;
    }
    return failures ? 1 : 0;
}
