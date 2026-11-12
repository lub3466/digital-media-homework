/*
 * tb_matmul.v — matmul.v 的 testbench
 *
 * 固定 A、B 两组 3x3 数据，延迟 10ns 等组合逻辑稳定后，
 * 把 9 个输出与 C 版的标准答案逐项比较。
 */
`timescale 1ns / 1ps

module tb_matmul;

    parameter N = 3;
    parameter W = 32;

    reg  [W-1:0] A  [0:N-1][0:N-1];
    reg  [W-1:0] B  [0:N-1][0:N-1];
    wire [W-1:0] C  [0:N-1][0:N-1];
    reg  [W-1:0] EXP[0:N-1][0:N-1];

    integer i, j, errs;

    matmul #(.N(N), .W(W)) dut (
        .A(A), .B(B), .C(C)
    );

    initial begin
        errs = 0;

        // A = [[1,2,3],[4,5,6],[7,8,9]]
        A[0][0]=1;  A[0][1]=2;  A[0][2]=3;
        A[1][0]=4;  A[1][1]=5;  A[1][2]=6;
        A[2][0]=7;  A[2][1]=8;  A[2][2]=9;

        // B = [[9,8,7],[6,5,4],[3,2,1]]
        B[0][0]=9;  B[0][1]=8;  B[0][2]=7;
        B[1][0]=6;  B[1][1]=5;  B[1][2]=4;
        B[2][0]=3;  B[2][1]=2;  B[2][2]=1;

        // 标准答案（与 matmul.c / NumPy 一致）
        EXP[0][0]=30;  EXP[0][1]=24;  EXP[0][2]=18;
        EXP[1][0]=84;  EXP[1][1]=69;  EXP[1][2]=54;
        EXP[2][0]=138; EXP[2][1]=114; EXP[2][2]=90;

        #10;   // 等组合逻辑稳定

        $display("C = A x B :");
        for (i = 0; i < N; i = i + 1)
            $display("  %4d %4d %4d", C[i][0], C[i][1], C[i][2]);

        for (i = 0; i < N; i = i + 1)
            for (j = 0; j < N; j = j + 1)
                if (C[i][j] !== EXP[i][j]) begin
                    $display("MISMATCH C[%0d][%0d] = %0d, expect %0d",
                             i, j, C[i][j], EXP[i][j]);
                    errs = errs + 1;
                end

        if (errs == 0)
            $display("OK: 9/9 elements match C version");
        else
            $display("FAIL: %0d mismatches", errs);

        $finish;
    end

endmodule
