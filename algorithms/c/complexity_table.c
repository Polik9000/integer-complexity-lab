/*
 * Exact integer complexity ||n|| for all 1 <= n <= N.
 *
 *   ||1|| = 1,  ||n|| = min( min_{d e = n, 2<=d<=e} ||d||+||e||,
 *                            min_{1<=a<=n/2}        ||a||+||n-a|| ).
 *
 * Multiplicative candidates are pushed forward (total work ~ N log N).
 * Additive candidates are pruned RIGOROUSLY: a value built from k ones is at
 * most 3^(k/3) (Selfridge), hence ||a||+||n-a|| >= 3 log_3(a(n-a)).  An
 * additive split can improve the current best b only if ||a||+||n-a|| <= b-1,
 * which requires (a(n-a))^3 <= 3^(b-1).  Since a(n-a) is increasing on
 * [1, n/2], the loop over a stops at the first a violating this.
 *
 * Usage: complexity_table N OUTFILE   (OUTFILE: N+1 bytes, byte n = ||n||, byte 0 = 0)
 * Prints a short summary (max value, sha-like checksum) to stdout.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef unsigned __int128 u128;

int main(int argc, char **argv) {
    if (argc != 3) { fprintf(stderr, "usage: %s N OUTFILE\n", argv[0]); return 2; }
    uint64_t N = strtoull(argv[1], NULL, 10);
    if (N < 1 || N > 4000000000ULL) { fprintf(stderr, "N out of range\n"); return 2; }

    /* lim[k] = largest P with P^3 <= 3^k  (k <= 80 keeps 3^k < 2^128) */
    uint64_t lim[81];
    u128 p3 = 1;
    for (int k = 0; k <= 80; k++) {
        uint64_t lo = 0, hi = 1ULL << 43;           /* (2^43)^3 = 2^129 > 3^80 */
        while (lo < hi) {
            uint64_t mid = lo + (hi - lo + 1) / 2;
            u128 c = (u128)mid * mid * mid;
            if (c <= p3) lo = mid; else hi = mid - 1;
        }
        lim[k] = lo;
        p3 *= 3;
    }

    uint8_t *c = malloc(N + 1);
    if (!c) { fprintf(stderr, "out of memory\n"); return 1; }
    for (uint64_t i = 0; i <= N; i++) c[i] = 255;
    c[0] = 0;
    c[1] = 1;
    uint64_t checksum = 1469598103934665603ULL;     /* FNV-1a over bytes 1..N */
    uint8_t maxv = 0;

    for (uint64_t n = 1; n <= N; n++) {
        if (n >= 2) {
            uint8_t best = c[n];                      /* multiplicative candidates */
            if (c[n - 1] + 1 < best) best = c[n - 1] + 1;   /* a = 1 */
            for (uint64_t a = 2; 2 * a <= n; a++) {
                if (best < 1 || best - 1 > 80) { fprintf(stderr, "bound overflow\n"); return 1; }
                if (a * (n - a) > lim[best - 1]) break;
                uint8_t v = c[a] + c[n - a];
                if (v < best) best = v;
            }
            c[n] = best;
        }
        /* push products n*d for d <= n */
        for (uint64_t d = 2; d <= n && d * n <= N; d++) {
            uint8_t v = c[d] + c[n];
            if (v < c[d * n]) c[d * n] = v;
        }
        if (c[n] > maxv) maxv = c[n];
        checksum ^= c[n]; checksum *= 1099511628211ULL;
    }

    FILE *f = fopen(argv[2], "wb");
    if (!f || fwrite(c, 1, N + 1, f) != N + 1) { fprintf(stderr, "write failed\n"); return 1; }
    fclose(f);
    printf("N=%llu max=%u fnv1a=%016llx\n", (unsigned long long)N, maxv, (unsigned long long)checksum);
    free(c);
    return 0;
}
