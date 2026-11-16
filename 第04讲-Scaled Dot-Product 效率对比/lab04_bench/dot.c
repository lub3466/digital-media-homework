/*
 * dot.c — C 版点积（仅标准库，-O2 编译）
 *
 * 用法：dot_c.exe <a.bin> <b.bin> <n>
 *
 * 计时协议与 Python / Rust 完全一致：读文件不计时；预热 10 轮后
 * 正式 200 轮，同时输出最小值与中位数；checksum 声明为 volatile 并被
 * printf 消费，防止 -O2 把整段循环当死代码删掉。
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define WARMUP 10
#define ROUNDS 200

static double *read_f64(const char *path, size_t *out_n)
{
    FILE *fp = fopen(path, "rb");
    if (!fp) { fprintf(stderr, "open failed: %s\n", path); exit(1); }
    fseek(fp, 0, SEEK_END);
    long bytes = ftell(fp);
    fseek(fp, 0, SEEK_SET);
    size_t n = (size_t)bytes / sizeof(double);
    double *buf = (double *)malloc(bytes);
    if (!buf) { fprintf(stderr, "malloc failed\n"); exit(1); }
    if (fread(buf, sizeof(double), n, fp) != n) {
        fprintf(stderr, "fread short read\n"); exit(1);
    }
    fclose(fp);
    *out_n = n;
    return buf;
}

static double dot(const double *a, const double *b, size_t n)
{
    double s = 0.0;
    for (size_t i = 0; i < n; i++)
        s += a[i] * b[i];
    return s;
}

static double now_sec(void)
{
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec * 1e-9;
}

static int cmp_double(const void *x, const void *y)
{
    double dx = *(const double *)x, dy = *(const double *)y;
    return (dx > dy) - (dx < dy);
}

int main(int argc, char **argv)
{
    if (argc != 4) {
        fprintf(stderr, "usage: dot_c <a.bin> <b.bin> <n>\n");
        return 2;
    }
    size_t na = 0, nb = 0, n = (size_t)atol(argv[3]);
    double *a = read_f64(argv[1], &na);
    double *b = read_f64(argv[2], &nb);
    if (na != n || nb != n) {
        fprintf(stderr, "length mismatch: %zu vs %zu\n", na, nb);
        return 2;
    }

    /* volatile：让编译器无法把 checksum 折叠成常量，逐轮真实计算 */
    volatile double checksum = 0.0;
    for (int i = 0; i < WARMUP; i++)
        checksum += dot(a, b, n);

    double times[ROUNDS];
    for (int i = 0; i < ROUNDS; i++) {
        double t0 = now_sec();
        checksum += dot(a, b, n);
        times[i] = now_sec() - t0;
    }

    qsort(times, ROUNDS, sizeof(double), cmp_double);
    double median = (times[ROUNDS / 2] + times[(ROUNDS - 1) / 2]) / 2.0;
    double minimum = times[0];   /* 排序后 times[0] 即最小值 */

    double result = dot(a, b, n);
    printf("lang=c n=%zu result=%.12f checksum=%.6f median_us=%.2f min_us=%.2f\n",
           n, result, checksum, median * 1e6, minimum * 1e6);

    free(a);
    free(b);
    return 0;
}
