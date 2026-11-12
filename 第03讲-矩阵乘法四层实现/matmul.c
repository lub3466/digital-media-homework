/*
 * matmul.c — 第 03 讲 矩阵乘法（C 版，三重循环）
 *
 * 3x3 整数矩阵 C = A x B，逐项与标准答案比对。
 * 乘法单独放在 matmul() 里，避免 -O2 把 A、B 直接常量折叠成结果，
 * 这样 -O0 / -O2 的 .s 才能看到真实的循环展开与向量化差异。
 *
 * 编译：gcc matmul.c -o matmul.exe
 * 运行：matmul.exe
 */
#include <stdio.h>

#define N 3

static int A[N][N] = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

static int B[N][N] = {
    {9, 8, 7},
    {6, 5, 4},
    {3, 2, 1}
};

/* 标准答案：先用 NumPy 算好，写死在这里做逐项比对 */
static int EXPECTED[N][N] = {
    { 30,  24,  18},
    { 84,  69,  54},
    {138, 114,  90}
};

/* 三重循环：i 行、j 列、k 累加下标 */
void matmul(int a[N][N], int b[N][N], int c[N][N])
{
    int i, j, k;
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++) {
            int s = 0;
            for (k = 0; k < N; k++) {
                s += a[i][k] * b[k][j];   /* 最内层的乘加 */
            }
            c[i][j] = s;
        }
    }
}

int main(void)
{
    int C[N][N];
    int i, j;
    int fail = 0;

    matmul(A, B, C);

    printf("C = A x B :\n");
    for (i = 0; i < N; i++) {
        for (j = 0; j < N; j++)
            printf("%4d ", C[i][j]);
        printf("\n");
    }

    for (i = 0; i < N; i++)
        for (j = 0; j < N; j++)
            if (C[i][j] != EXPECTED[i][j]) {
                printf("MISMATCH [%d][%d]: got %d, want %d\n",
                       i, j, C[i][j], EXPECTED[i][j]);
                fail = 1;
            }

    printf(fail ? "FAIL\n" : "OK: 9/9 elements match NumPy golden answer\n");
    return fail;
}
