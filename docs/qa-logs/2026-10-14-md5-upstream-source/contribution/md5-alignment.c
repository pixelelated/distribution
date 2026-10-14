/* SPDX-License-Identifier: MIT
 * Cross-compile with the actual libretro-common md5.c and compare each emitted
 * digest with an independent implementation. No game, account or file input.
 */
#include <lrc_hash.h>
#include <stddef.h>
#include <stdio.h>

int main(void)
{
    static const size_t lengths[] = {0, 1, 55, 56, 63, 64, 65, 127, 128, 129, 1024};
    union { MD5_u32plus aligned; unsigned char bytes[1032]; } input;
    unsigned char digest[16];
    unsigned offset, split, i;
    size_t l, n;
    for (offset = 0; offset < 8; ++offset) {
        for (i = 0; i < 1024; ++i) input.bytes[offset + i] = (unsigned char)(i * 13 + 7);
        for (l = 0; l < sizeof(lengths) / sizeof(lengths[0]); ++l) {
            n = lengths[l];
            for (split = 0; split < 3; ++split) {
                const size_t first = split == 0 ? n : split == 1 ? n / 2 : (n > 1 ? 1 : 0);
                MD5_CTX ctx;
                MD5_Init(&ctx);
                MD5_Update(&ctx, input.bytes + offset, (unsigned long)first);
                MD5_Update(&ctx, input.bytes + offset + first, (unsigned long)(n - first));
                MD5_Final(digest, &ctx);
                printf("%u %zu %u ", offset, n, split);
                for (i = 0; i < sizeof(digest); ++i) printf("%02x", digest[i]);
                putchar('\n');
            }
        }
    }
    return 0;
}
