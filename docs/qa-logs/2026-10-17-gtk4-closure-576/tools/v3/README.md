Version 3 requires all package/sysroot critical pairs to match exact normalized ELF headers, program headers, LOAD geometry and loaded byte hashes; only e_shoff/e_shnum/e_shstrndx differ permissibly due to stripping.
Both absent build IDs are recorded, never treated as matching IDs. No target execution, target strip, compiler, or producer is used.
Original v1 and v2 failures and packets remain retained.
