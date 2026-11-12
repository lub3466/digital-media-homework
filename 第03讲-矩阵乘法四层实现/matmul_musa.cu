/*
 * matmul_musa.cu — matmul.cu 的 MUSA 迁移版
 *
 * 摩尔线程 MUSA 是 CUDA 的国产兼容层：API 命名把 cuda 前缀换成 musa，
 * 编程模型（grid/block/thread、核函数、显存拷贝）完全一致。
 * 本文件由 matmul.cu 只替换 cuda 前缀得到，未改动任何算法。
 *
 * 编译（需摩尔线程 MUSA SDK）：mcc matmul_musa.cu -o matmul_musa
 */
#include <stdio.h>
#include <musa_runtime.h>

#define N 3
#define BLOCK 32

__global__ void mmul_kernel(const int *A, const int *B, int *C)
{
    int i = blockIdx.y * blockDim.y + threadIdx.y;
    int j = blockIdx.x * blockDim.x + threadIdx.x;

    if (i < N && j < N) {
        int s = 0;
        for (int k = 0; k < N; k++)
            s += A[i * N + k] * B[k * N + j];
        C[i * N + j] = s;
    }
}

int main(void)
{
    int hA[N * N] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    int hB[N * N] = {9, 8, 7, 6, 5, 4, 3, 2, 1};
    int hC[N * N] = {0};
    int expected[N * N] = {30, 24, 18, 84, 69, 54, 138, 114, 90};

    int *dA, *dB, *dC;
    musaMalloc(&dA, sizeof(int) * N * N);
    musaMalloc(&dB, sizeof(int) * N * N);
    musaMalloc(&dC, sizeof(int) * N * N);

    musaMemcpy(dA, hA, sizeof(int) * N * N, musaMemcpyHostToDevice);
    musaMemcpy(dB, hB, sizeof(int) * N * N, musaMemcpyHostToDevice);

    dim3 block(BLOCK, BLOCK);
    dim3 grid((N + BLOCK - 1) / BLOCK, (N + BLOCK - 1) / BLOCK);

    mmul_kernel<<<grid, block>>>(dA, dB, dC);
    musaDeviceSynchronize();

    musaMemcpy(hC, dC, sizeof(int) * N * N, musaMemcpyDeviceToHost);

    printf("grid = (%d, %d), block = (%d, %d), total threads = %d\n",
           grid.x, grid.y, block.x, block.y, grid.x * grid.y * block.x * block.y);
    printf("C = A x B :\n");
    int fail = 0;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            printf("%4d ", hC[i * N + j]);
            if (hC[i * N + j] != expected[i * N + j])
                fail = 1;
        }
        printf("\n");
    }
    printf(fail ? "FAIL\n" : "OK: 9/9 elements match NumPy golden answer\n");

    musaFree(dA);
    musaFree(dB);
    musaFree(dC);
    return fail;
}
