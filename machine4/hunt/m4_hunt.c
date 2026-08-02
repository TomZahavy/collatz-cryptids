/* Machine 4 -- exact accelerated excursions in C (u128), port of m4_accel.py.
 *
 * Semantics are EXACTLY m4_accel.excursion(): T5 clean table, cascade batched
 * by T3's closed form, returns/halts at the six ending channels, exact base-
 * step counting.  Cross-checked value-for-value against the Python (itself
 * verified step-exact against m4_base.step).
 *
 * modes:
 *   verify                      read odd starts (decimal) on stdin; for each
 *                               print "out val base rounds exit_d"
 *   orbit  A ROUNDS_BUDGET      run the true orbit from section value A until
 *                               HALT or budget exhausted; print every visit
 *   pvisit K N CAP SEED         N random odd a in [2^K, 2^{K+1}); excursion
 *                               each with round cap CAP; print summary row
 * Values guarded below 2^100; exceeding it aborts the run loudly.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

typedef unsigned __int128 u128;

static const int OUT_RETURN = 0, OUT_HALT = 1, OUT_CAP = 2, OUT_OVERFLOW = 3;
static const char *OUTNAME[] = {"RETURN", "HALT", "CAP", "OVERFLOW"};

static u128 GUARD;                       /* 2^100 */

/* ---------- u128 helpers ---------- */
static int bitlen(u128 v) {
    int n = 0;
    while (v) { v >>= 1; n++; }
    return n;
}
static char *u128s(u128 v, char *buf) {  /* decimal, buf >= 40 bytes */
    char t[50]; int i = 0;
    if (!v) { strcpy(buf, "0"); return buf; }
    while (v) { t[i++] = '0' + (int)(v % 10); v /= 10; }
    int j = 0; while (i) buf[j++] = t[--i];
    buf[j] = 0; return buf;
}
static u128 parse_u128(const char *s) {
    u128 v = 0;
    while (*s >= '0' && *s <= '9') { v = v * 10 + (u128)(*s - '0'); s++; }
    return v;
}

/* ---------- RNG (splitmix64) ---------- */
static uint64_t sm_state;
static uint64_t sm_next(void) {
    uint64_t z = (sm_state += 0x9e3779b97f4a7c15ULL);
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
    z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
    return z ^ (z >> 31);
}

/* ---------- one excursion ---------- */
typedef struct {
    int out;            /* OUT_* */
    u128 val;           /* return value (OUT_RETURN) */
    u128 base;          /* exact base steps */
    u128 rounds;        /* accelerated rounds */
    int exit_d;         /* y-x at the ending configuration; 99 if none */
    int exit_m8;        /* source a mod 8 at the ending step; -1 if none */
    u128 cap_x, cap_y;  /* state at cap (OUT_CAP only) */
} exres;

static exres excursion(u128 a, u128 cap /* 0 = none */) {
    exres r; memset(&r, 0, sizeof r);
    u128 x = a, y = 1, base = 0, rounds = 0;
    r.exit_d = 99; r.exit_m8 = -1;
    for (;;) {
        if (cap && rounds >= cap) {
            r.out = OUT_CAP; r.base = base; r.rounds = rounds;
            r.val = x; r.exit_d = (int)(y & 0xff);  /* not used */
            r.cap_x = x; r.cap_y = y;
            return r;
        }
        if (x > GUARD || y > GUARD) {
            r.out = OUT_OVERFLOW; r.base = base; r.rounds = rounds; return r;
        }
        rounds++;
        if (y <= x) {                                /* the two m-rules */
            if (y & 1) {
                u128 nx = 2*y + 1, ny = x - y + 3;   /* ny >= 3 */
                x = nx; y = ny; base++;
            } else {
                u128 nx = 2*y + 3, ny = x - y;
                base++;
                if (ny == 1) {                       /* y = x-1: return */
                    r.out = OUT_RETURN; r.val = nx; r.base = base;
                    r.rounds = rounds; r.exit_d = -1; r.exit_m8 = (int)(x & 7);
                    return r;
                }
                x = nx; y = ny;
            }
            continue;
        }
        u128 d = y - x;
        if (d >= 5) {
            if (d == 5) {                            /* single step, returns */
                r.out = OUT_RETURN; r.val = 2*x + 5; r.base = base + 1;
                r.rounds = rounds; r.exit_d = 5; r.exit_m8 = (int)(x & 7);
                return r;
            }
            /* cascade batch: least j>=1 with y + j < (2^{j+1}-1)(x+5) */
            u128 s = x + 5;
            int j = bitlen(y / s + 1) - 1;
            if (j < 1) j = 1;
            while (y + (u128)j >= (((u128)1 << (j+1)) - 1) * s) j++;
            while (j > 1 && y + (u128)(j-1) < (((u128)1 << j) - 1) * s) j--;
            u128 p = (u128)1 << j;
            u128 x2 = p * s - 5, y2 = y - (p - 1) * s + (u128)j;
            base += (u128)j;
            if (y2 == 1) {                           /* last step was b=a+5 */
                r.out = OUT_RETURN; r.val = x2; r.base = base;
                r.rounds = rounds; r.exit_d = 5;
                r.exit_m8 = (int)(((x2 - 5) >> 1) & 7);
                return r;
            }
            x = x2; y = y2;
            continue;
        }
        /* d in {1,2,3,4}: near-line dispatch */
        base++;
        if (d == 3) {
            r.out = OUT_HALT; r.base = base; r.rounds = rounds;
            r.exit_d = 3; r.exit_m8 = (int)(x & 7);
            return r;
        }
        r.out = OUT_RETURN;
        r.val = (d == 1) ? 2*x - 1 : (d == 2 ? 2*x + 5 : 2*x + 3);
        r.base = base; r.rounds = rounds;
        r.exit_d = (int)d; r.exit_m8 = (int)(x & 7);
        return r;
    }
}

/* ---------- modes ---------- */
static int mode_verify(u128 cap) {
    char line[64], b1[44], b2[44], b3[44], b4[44];
    while (fgets(line, sizeof line, stdin)) {
        u128 a = parse_u128(line);
        if (!a) continue;
        exres r = excursion(a, cap);
        if (r.out == OUT_CAP)
            printf("CAP %s %s %s %s\n", u128s(r.cap_x, b1),
                   u128s(r.cap_y, b4), u128s(r.base, b2),
                   u128s(r.rounds, b3));
        else
            printf("%s %s %s %s %d\n", OUTNAME[r.out],
                   r.out == OUT_RETURN ? u128s(r.val, b1) : "-",
                   u128s(r.base, b2), u128s(r.rounds, b3), r.exit_d);
    }
    return 0;
}

static int mode_orbit(u128 a, u128 budget) {
    char b1[44], b2[44], b3[44], b4[44], b5[44];
    u128 tot_rounds = 0, tot_base = 0;
    long visit = 0;
    time_t t0 = time(NULL);
    printf("# orbit from a=%s, round budget %s\n",
           u128s(a, b1), u128s(budget, b2));
    printf("# visit  a  bits  exit_d  exit_m8  exc_base  exc_rounds  "
           "cum_base  cum_rounds  secs\n");
    fflush(stdout);
    for (;;) {
        if (tot_rounds >= budget) {
            printf("BUDGET-EXHAUSTED at a=%s (between excursions)\n",
                   u128s(a, b1));
            return 0;
        }
        u128 left = budget - tot_rounds;
        exres r = excursion(a, left);
        tot_rounds += r.rounds; tot_base += r.base;
        if (r.out == OUT_CAP) {
            printf("BUDGET-EXHAUSTED mid-excursion from a=%s after %s rounds "
                   "(%s base steps into it); cum_base=%s cum_rounds=%s\n",
                   u128s(a, b1), u128s(r.rounds, b2), u128s(r.base, b3),
                   u128s(tot_base, b4), u128s(tot_rounds, b5));
            return 0;
        }
        if (r.out == OUT_OVERFLOW) {
            printf("OVERFLOW (values passed 2^100) from a=%s\n", u128s(a, b1));
            return 0;
        }
        if (r.out == OUT_HALT) {
            printf("*** HALT ***  from section value a=%s after %s base steps "
                   "of that excursion; cumulative base steps %s, "
                   "cumulative rounds %s, at visit %ld\n",
                   u128s(a, b1), u128s(r.base, b2), u128s(tot_base, b3),
                   u128s(tot_rounds, b4), visit);
            return 0;
        }
        visit++;
        printf("visit %ld  %s  %d  %+d  %d  %s  %s  ",
               visit, u128s(r.val, b1), bitlen(r.val), r.exit_d, r.exit_m8,
               u128s(r.base, b2), u128s(r.rounds, b3));
        printf("%s  ", u128s(tot_base, b1));
        printf("%s  %ld\n", u128s(tot_rounds, b2), (long)(time(NULL) - t0));
        fflush(stdout);
        a = r.val;
    }
}

static int mode_pvisit(int K, long N, u128 cap, uint64_t seed, int m16) {
    sm_state = seed * 0x100000001b3ULL + (uint64_t)K;
    long halts = 0, rets = 0, caps = 0, ovf = 0;
    long d_hist[8] = {0};        /* -1,1,2,3,4,5 -> idx 0..5 */
    long m8_3 = 0, m8_7 = 0;
    double sum_l2 = 0, max_l2 = 0;         /* log2(val/a) over returns */
    double sum_rounds = 0, sum_base = 0, max_rounds = 0;
    char b1[44];
    for (long i = 0; i < N; i++) {
        /* random odd a in [2^K, 2^{K+1}) */
        u128 a;
        if (K <= 62) {
            uint64_t m = (K == 0) ? 0 : (sm_next() & ((1ULL << K) - 1));
            a = ((u128)1 << K) | (u128)m | 1;
        } else {
            u128 m = (((u128)sm_next() << 64) | sm_next()) &
                     (((u128)1 << K) - 1);
            a = ((u128)1 << K) | m | 1;
        }
        if (m16 >= 0) a = (a & ~(u128)15) | (u128)m16;   /* force a mod 16 */
        exres r = excursion(a, cap);
        sum_rounds += (double)r.rounds; sum_base += (double)r.base;
        if ((double)r.rounds > max_rounds) max_rounds = (double)r.rounds;
        if (r.out == OUT_CAP) { caps++; continue; }
        if (r.out == OUT_OVERFLOW) { ovf++; continue; }
        if (r.exit_m8 == 3) m8_3++; else if (r.exit_m8 == 7) m8_7++;
        int idx = r.exit_d == -1 ? 0 : r.exit_d;   /* 1..5 map to 1..5 */
        if (idx >= 0 && idx <= 5) d_hist[idx]++;
        if (r.out == OUT_HALT) { halts++; continue; }
        rets++;
        double l2 = (double)bitlen(r.val) - (double)bitlen(a);  /* coarse */
        /* refined log2 ratio */
        {
            double va = (double)(uint64_t)(a >> (K > 50 ? K - 50 : 0));
            double vv;
            int bv = bitlen(r.val);
            int sh = bv > 50 ? bv - 50 : 0;
            vv = (double)(uint64_t)(r.val >> sh);
            l2 = (vv > 0 && va > 0)
                 ? ((double)sh - (double)(K > 50 ? K - 50 : 0)) +
                   (__builtin_log2(vv) - __builtin_log2(va)) : l2;
        }
        sum_l2 += l2; if (l2 > max_l2) max_l2 = l2;
    }
    long dec = halts + rets;
    printf("k=%2d n=%ld decided=%ld halts=%ld p=%.4f cap=%ld ovf=%ld  "
           "d[-1,1,2,3,4,5]=%ld,%ld,%ld,%ld,%ld,%ld  m8[3]=%ld m8[7]=%ld  "
           "E[l2ratio]=%.3f max_l2=%.1f  E[rounds]=%.3g max_rounds=%.3g "
           "E[base]=%.3g E[rounds]/2^k=%.4f\n",
           K, N, dec, halts, dec ? (double)halts / (double)dec : 0.0,
           caps, ovf,
           d_hist[0], d_hist[1], d_hist[2], d_hist[3], d_hist[4], d_hist[5],
           m8_3, m8_7,
           rets ? sum_l2 / rets : 0.0, max_l2,
           sum_rounds / N, max_rounds, sum_base / N,
           (sum_rounds / N) / (double)((u128)1 << K));
    fflush(stdout);
    (void)b1;
    return 0;
}

int main(int argc, char **argv) {
    GUARD = ((u128)1) << 100;
    if (argc >= 2 && !strcmp(argv[1], "verify"))
        return mode_verify(argc >= 3 ? parse_u128(argv[2]) : 0);
    if (argc >= 4 && !strcmp(argv[1], "orbit"))
        return mode_orbit(parse_u128(argv[2]), parse_u128(argv[3]));
    if (argc >= 6 && !strcmp(argv[1], "pvisit"))
        return mode_pvisit(atoi(argv[2]), atol(argv[3]),
                           parse_u128(argv[4]),
                           (uint64_t)strtoull(argv[5], NULL, 10),
                           argc >= 7 ? atoi(argv[6]) : -1);
    fprintf(stderr, "usage: m4_hunt verify|orbit A BUDGET|"
                    "pvisit K N CAP SEED\n");
    return 2;
}
