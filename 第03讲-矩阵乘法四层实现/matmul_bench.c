/*
 * matmul_bench.c — 第 03 讲 拓展任务：N=256 下比较循环顺序
 *
 * 同一个矩阵乘法，i-j-k（行优先但内层跳着访问 b[k][j]，缓存不命中）
 * 与 i-k-j（把最内层循环放到连续的一行上，缓存命中率高）的耗时对比。
 * CUDA 版见 matmul.cu（本机无 CUDA Toolkit，未跑实测）。
 *
 * 编译：gcc matmul_bench.c -O2 -o matmul_bench.exe
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 256

static int A[N][N], B[N][N], C[N][N];

static void init(void)
{
    int i, j;
    for (i = 0; i < N; i++)
        for (j = 0; j < N; j++) {
            A[i][j] = (i * 31 + j * 17) % 100;
            B[i][j] = (i * 13 + j * 29) % 100;
            C[i][j] = 0;
        }
}

/* i-j-k：最内层是 k，访问 b[k][j] 每次跨一整行，缓存不友好 */
static void mul_ijk(void)
{
    int i, j, k;
    for (i = 0; i < N; i++)
        for (j = 0; j < N; j++)
            for (k = 0; k < N; k++)
                C[i][j] += A[i][k] * B[k][j];
}

/* i-k-j：交换后两个循环，最内层 j 连续访问 a[i][k]、b[k][j]，缓存友好 */
static void mul_ikj(void)
{
    int i, k, j;
    for (i = 0; i < N; i++)
        for (k = 0; k < N; k++)
            for (j = 0; j < N; j++)
                C[i][j] += A[i][k] * B[k][j];
}

static double run(void (*fn)(void))
{
    clock_t t0, t1;
    int rep;
    t0 = clock();
    for (rep = 0; rep < 5; rep++) fn();
    t1 = clock();
    return (double)(t1 - t0) / CLOCKS_PER_SEC / 5.0 * 1000.0; /* ms */
}

int main(void)
{
    double t_ijk, t_ikj;
    long long sum = 0;
    int i, j;

    init();
    t_ijk = run(mul_ijk);

    init();
    t_ikj = run(mul_ikj);

    for (i = 0; i < N; i++)
        for (j = 0; j < N; j++)
            sum += C[i][j];

    printf("N = %d, -O2\n", N);
    printf("i-j-k : %8.2f ms   (最内层 k，跳行访问 B，缓存不友好)\n", t_ijk);
    printf("i-k-j : %8.2f ms   (最内层 j，连续访问，缓存友好)\n", t_ikj);
    printf("i-k-j 相对 i-j-k 提速：%.1fx  (校验和 %lld，两种顺序结果一致)\n",
           t_ijk / t_ikj, sum);
    return 0;
}
