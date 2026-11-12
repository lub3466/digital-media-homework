/*
 * matmul.cu — 第 03 讲 矩阵乘法（CUDA 版，一个线程算一个 C[i][j]）
 *
 * blockDim = 32，grid = ceil(N/32) x ceil(N/32) = 1 x 1，
 * 即 1 个块、32x32 = 1024 个线程，其中只有 9 个线程真正干活，
 * 其余线程靠 i < N && j < N 的边界判断挡在核函数外面。
 *
 * 编译（需 CUDA Toolkit）：nvcc matmul.cu -o matmul_cuda
 * 运行：matmul_cuda
 */
#include <stdio.h>
#include <cuda_runtime.h>

#define N 3
#define BLOCK 32

__global__ void mmul_kernel(const int *A, const int *B, int *C)
{
    int i = blockIdx.y * blockDim.y + threadIdx.y;
    int j = blockIdx.x * blockDim.x + threadIdx.x;

    if (i < N && j < N) {          /* 越界判断，防止读写越界 */
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
    cudaMalloc(&dA, sizeof(int) * N * N);
    cudaMalloc(&dB, sizeof(int) * N * N);
    cudaMalloc(&dC, sizeof(int) * N * N);

    cudaMemcpy(dA, hA, sizeof(int) * N * N, cudaMemcpyHostToDevice);
    cudaMemcpy(dB, hB, sizeof(int) * N * N, cudaMemcpyHostToDevice);

    dim3 block(BLOCK, BLOCK);
    dim3 grid((N + BLOCK - 1) / BLOCK, (N + BLOCK - 1) / BLOCK);

    mmul_kernel<<<grid, block>>>(dA, dB, dC);
    cudaDeviceSynchronize();

    cudaMemcpy(hC, dC, sizeof(int) * N * N, cudaMemcpyDeviceToHost);

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

    cudaFree(dA);
    cudaFree(dB);
    cudaFree(dC);
    return fail;
}
