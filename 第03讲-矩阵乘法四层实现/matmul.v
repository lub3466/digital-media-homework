/*
 * matmul.v — 第 03 讲 矩阵乘法（Verilog 版，纯组合逻辑）
 *
 * parameter N = 3，用 generate + genvar 展开出 N*N 个输出单元，
 * 每个单元由 (N-1) 个加法器和 N 个乘法器构成，共 9 个乘法器、6 个加法器。
 * 全部用 assign 写组合逻辑，没有任何时钟、没有寄存器。
 *
 * 仿真：iverilog -g2012 -o tb.vvp tb_matmul.v matmul.v
 */
module matmul
#(
    parameter N = 3,
    parameter W = 32
)
(
    input  wire [W-1:0] A [0:N-1][0:N-1],
    input  wire [W-1:0] B [0:N-1][0:N-1],
    output wire [W-1:0] C [0:N-1][0:N-1]
);

    genvar i, j, k;
    generate
        for (i = 0; i < N; i = i + 1) begin : row
            for (j = 0; j < N; j = j + 1) begin : col
                /* 每个 C[i][j] 是一条乘加链：acc[k] = acc[k-1] + A[i][k]*B[k][j] */
                wire [W-1:0] acc [0:N-1];
                assign acc[0] = A[i][0] * B[0][j];
                for (k = 1; k < N; k = k + 1) begin : mac
                    assign acc[k] = acc[k-1] + A[i][k] * B[k][j];
                end
                assign C[i][j] = acc[N-1];
            end
        end
    endgenerate

endmodule
