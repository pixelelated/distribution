// T20 Q7 (#667): EmulationStation's padding() (rvz_hash.cpp:38-42, :66-98 at 16dbac5211, verbatim)
// against Dolphin's LaggedFibonacciGenerator as retained in docs/qa-logs/2026-10-14-proxy-rvz-source/
// (SetSeed, Initialize's tweak and swap, Forward x4, Forward(count), GetBytes), on a little-endian host.
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <random>
#include <vector>
constexpr uint64_t Sector = 0x8000;
uint32_t be32(const uint8_t* p)
{
    return (uint32_t(p[0]) << 24) | (uint32_t(p[1]) << 16) |
        (uint32_t(p[2]) << 8) | p[3];
}
void padding(const uint8_t* seed, uint64_t offset, uint8_t* out, size_t size)
{
    std::array<uint32_t, 521> words{};
    for (size_t i = 0; i < 17; ++i)
        words[i] = be32(seed + 4 * i);
    for (size_t i = 17; i < words.size(); ++i)
        words[i] = (words[i - 17] << 23) ^ (words[i - 16] >> 9) ^ words[i - 1];
    const auto advance = [&]() {
        for (size_t i = 0; i < 32; ++i)
            words[i] ^= words[i + words.size() - 32];
        for (size_t i = 32; i < words.size(); ++i)
            words[i] ^= words[i - 32];
    };
    for (unsigned i = 0; i < 4; ++i)
        advance();
    size_t byteIndex = static_cast<size_t>(offset % Sector);
    while (byteIndex >= words.size() * 4)
    {
        advance();
        byteIndex -= words.size() * 4;
    }
    const unsigned shifts[] = {24, 18, 8, 0};
    for (size_t i = 0; i < size; ++i)
    {
        if (byteIndex == words.size() * 4)
        {
            advance();
            byteIndex = 0;
        }
        out[i] = static_cast<uint8_t>(words[byteIndex / 4] >> shifts[byteIndex % 4]);
        ++byteIndex;
    }
}
static uint32_t swap32(uint32_t x){ return __builtin_bswap32(x); }
struct Dolphin {   // DiscIO::LaggedFibonacciGenerator, transcribed
  static constexpr size_t K = 521, J = 32, SEED = 17;
  std::array<uint32_t, K> b{}; size_t pos = 0;
  void Forward(){ for (size_t i = 0; i < J; ++i) b[i] ^= b[i + K - J]; for (size_t i = J; i < K; ++i) b[i] ^= b[i - J]; }
  void SetSeed(const uint8_t* s){ pos = 0; for (size_t i = 0; i < SEED; ++i) { uint32_t v; memcpy(&v, s + 4*i, 4); b[i] = swap32(v); }
    for (size_t i = SEED; i < K; ++i) b[i] = (b[i-17] << 23) ^ (b[i-16] >> 9) ^ b[i-1];
    for (auto& x : b) x = swap32((x & 0xFF00FFFF) | ((x >> 2) & 0x00FF0000));
    for (int i = 0; i < 4; ++i) Forward(); }
  void Forward(size_t count){ pos += count; while (pos >= K*4) { Forward(); pos -= K*4; } }
  void GetBytes(size_t n, uint8_t* out){ while (n) { size_t len = std::min(n, K*4 - pos); memcpy(out, reinterpret_cast<uint8_t*>(b.data()) + pos, len);
      pos += len; n -= len; out += len; if (pos == K*4) { Forward(); pos = 0; } } }
};
int main(){
  std::mt19937_64 rng(667); int cases = 0, mismatches = 0, unaligned = 0;
  for (int t = 0; t < 4000; ++t) {
    uint8_t seed[68]; for (auto& c : seed) c = (uint8_t) rng();
    uint64_t offset = rng() % (uint64_t(1) << 33); size_t size = 1 + rng() % 6000;
    if (offset % 4) unaligned++;
    std::vector<uint8_t> es(size), dol(size);
    padding(seed, offset, es.data(), size);
    Dolphin d; d.SetSeed(seed); d.Forward(offset % Sector); d.GetBytes(size, dol.data());
    cases++; if (es != dol) mismatches++;
  }
  // and the control: the "16" a reader might expect differs from both
  printf("Q7 padding: cases=%d unaligned=%d mismatches=%d\n", cases, unaligned, mismatches);
  return mismatches != 0;
}
