def classify(h):
    if h[:4] != b"\x7fELF": return None
    if len(h) < 20: return {"kind": "opaque-ELF-fixture", "reason": "short header", "elf_type": None}
    if h[4] not in (1,2): return {"kind": "opaque-ELF-fixture", "reason": "invalid class", "elf_type": None}
    if h[5] not in (1,2): return {"kind": "opaque-ELF-fixture", "reason": "invalid byte order", "elf_type": None}
    return {"kind": "ELF-header", "elf_type": int.from_bytes(h[16:18], "little" if h[5]==1 else "big")}
