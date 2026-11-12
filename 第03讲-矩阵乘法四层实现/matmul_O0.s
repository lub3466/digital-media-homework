	.file	"matmul.c"
 # GNU C23 (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r3) version 16.2.0 (x86_64-w64-mingw32)
 #	compiled by GNU C version 16.2.0, GMP version 6.3.0, MPFR version 4.2.2, MPC version 1.4.1, isl version isl-0.28-GMP

 # GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
 # options passed: -mtune=generic -march=x86-64 -O0
	.text
	.data
	.align 32
A:
	.long	1
	.long	2
	.long	3
	.long	4
	.long	5
	.long	6
	.long	7
	.long	8
	.long	9
	.align 32
B:
	.long	9
	.long	8
	.long	7
	.long	6
	.long	5
	.long	4
	.long	3
	.long	2
	.long	1
	.align 32
EXPECTED:
	.long	30
	.long	24
	.long	18
	.long	84
	.long	69
	.long	54
	.long	138
	.long	114
	.long	90
	.text
	.globl	matmul
	.def	matmul;	.scl	2;	.type	32;	.endef
	.seh_proc	matmul
matmul:
	pushq	%rbp	 #
	.seh_pushreg	%rbp
	movq	%rsp, %rbp	 #,
	.seh_setframe	%rbp, 0
	subq	$16, %rsp	 #,
	.seh_stackalloc	16
	.seh_endprologue
	movq	%rcx, 16(%rbp)	 # a, a
	movq	%rdx, 24(%rbp)	 # b, b
	movq	%r8, 32(%rbp)	 # c, c
 # matmul.c:38:     for (i = 0; i < N; i++) {
	movl	$0, -4(%rbp)	 #, i
 # matmul.c:38:     for (i = 0; i < N; i++) {
	jmp	.L2	 #
.L7:
 # matmul.c:39:         for (j = 0; j < N; j++) {
	movl	$0, -8(%rbp)	 #, j
 # matmul.c:39:         for (j = 0; j < N; j++) {
	jmp	.L3	 #
.L6:
 # matmul.c:40:             int s = 0;
	movl	$0, -16(%rbp)	 #, s
 # matmul.c:41:             for (k = 0; k < N; k++) {
	movl	$0, -12(%rbp)	 #, k
 # matmul.c:41:             for (k = 0; k < N; k++) {
	jmp	.L4	 #
.L5:
 # matmul.c:42:                 s += a[i][k] * b[k][j];   /* 最内层的乘加 */
	movl	-4(%rbp), %eax	 # i, tmp110
	movslq	%eax, %rdx	 # tmp110, _1
	movq	%rdx, %rax	 # _1, _2
	addq	%rax, %rax	 # _2
	addq	%rdx, %rax	 # _1, _2
	salq	$2, %rax	 #, tmp112
	movq	%rax, %rdx	 # _2, _2
	movq	16(%rbp), %rax	 # a, tmp113
	addq	%rax, %rdx	 # tmp113, _3
 # matmul.c:42:                 s += a[i][k] * b[k][j];   /* 最内层的乘加 */
	movl	-12(%rbp), %eax	 # k, tmp115
	cltq
	movl	(%rdx,%rax,4), %ecx	 # (*_3)[k_15], _4
 # matmul.c:42:                 s += a[i][k] * b[k][j];   /* 最内层的乘加 */
	movl	-12(%rbp), %eax	 # k, tmp116
	movslq	%eax, %rdx	 # tmp116, _5
	movq	%rdx, %rax	 # _5, _6
	addq	%rax, %rax	 # _6
	addq	%rdx, %rax	 # _5, _6
	salq	$2, %rax	 #, tmp118
	movq	%rax, %rdx	 # _6, _6
	movq	24(%rbp), %rax	 # b, tmp119
	addq	%rax, %rdx	 # tmp119, _7
 # matmul.c:42:                 s += a[i][k] * b[k][j];   /* 最内层的乘加 */
	movl	-8(%rbp), %eax	 # j, tmp121
	cltq
	movl	(%rdx,%rax,4), %eax	 # (*_7)[j_14], _8
 # matmul.c:42:                 s += a[i][k] * b[k][j];   /* 最内层的乘加 */
	imull	%ecx, %eax	 # _4, _9
 # matmul.c:42:                 s += a[i][k] * b[k][j];   /* 最内层的乘加 */
	addl	%eax, -16(%rbp)	 # _9, s
 # matmul.c:41:             for (k = 0; k < N; k++) {
	addl	$1, -12(%rbp)	 #, k
.L4:
 # matmul.c:41:             for (k = 0; k < N; k++) {
	cmpl	$2, -12(%rbp)	 #, k
	jle	.L5	 #,
 # matmul.c:44:             c[i][j] = s;
	movl	-4(%rbp), %eax	 # i, tmp122
	movslq	%eax, %rdx	 # tmp122, _10
	movq	%rdx, %rax	 # _10, _11
	addq	%rax, %rax	 # _11
	addq	%rdx, %rax	 # _10, _11
	salq	$2, %rax	 #, tmp124
	movq	%rax, %rdx	 # _11, _11
	movq	32(%rbp), %rax	 # c, tmp125
	leaq	(%rdx,%rax), %rcx	 #, _12
 # matmul.c:44:             c[i][j] = s;
	movl	-8(%rbp), %eax	 # j, tmp127
	cltq
	movl	-16(%rbp), %edx	 # s, tmp128
	movl	%edx, (%rcx,%rax,4)	 # tmp128, (*_12)[j_14]
 # matmul.c:39:         for (j = 0; j < N; j++) {
	addl	$1, -8(%rbp)	 #, j
.L3:
 # matmul.c:39:         for (j = 0; j < N; j++) {
	cmpl	$2, -8(%rbp)	 #, j
	jle	.L6	 #,
 # matmul.c:38:     for (i = 0; i < N; i++) {
	addl	$1, -4(%rbp)	 #, i
.L2:
 # matmul.c:38:     for (i = 0; i < N; i++) {
	cmpl	$2, -4(%rbp)	 #, i
	jle	.L7	 #,
 # matmul.c:47: }
	nop	
	nop	
	addq	$16, %rsp	 #,
	popq	%rbp	 #
	ret	
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "C = A x B :\0"
.LC1:
	.ascii "%4d \0"
	.align 8
.LC2:
	.ascii "MISMATCH [%d][%d]: got %d, want %d\12\0"
.LC3:
	.ascii "FAIL\12\0"
	.align 8
.LC4:
	.ascii "OK: 9/9 elements match NumPy golden answer\12\0"
	.text
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
	pushq	%rbp	 #
	.seh_pushreg	%rbp
	movq	%rsp, %rbp	 #,
	.seh_setframe	%rbp, 0
	subq	$96, %rsp	 #,
	.seh_stackalloc	96
	.seh_endprologue
 # matmul.c:50: {
	call	__main	 #
 # matmul.c:53:     int fail = 0;
	movl	$0, -12(%rbp)	 #, fail
 # matmul.c:55:     matmul(A, B, C);
	leaq	-48(%rbp), %rcx	 #, tmp106
	leaq	B(%rip), %rdx	 #, tmp107
	leaq	A(%rip), %rax	 #, tmp108
	movq	%rcx, %r8	 # tmp106,
	movq	%rax, %rcx	 # tmp108,
	call	matmul	 #
 # matmul.c:57:     printf("C = A x B :\n");
	leaq	.LC0(%rip), %rax	 #, tmp109
	movq	%rax, %rcx	 # tmp109,
	call	puts	 #
 # matmul.c:58:     for (i = 0; i < N; i++) {
	movl	$0, -4(%rbp)	 #, i
 # matmul.c:58:     for (i = 0; i < N; i++) {
	jmp	.L9	 #
.L12:
 # matmul.c:59:         for (j = 0; j < N; j++)
	movl	$0, -8(%rbp)	 #, j
 # matmul.c:59:         for (j = 0; j < N; j++)
	jmp	.L10	 #
.L11:
 # matmul.c:60:             printf("%4d ", C[i][j]);
	movl	-8(%rbp), %eax	 # j, tmp111
	movslq	%eax, %rcx	 # tmp111, tmp110
	movl	-4(%rbp), %eax	 # i, tmp113
	movslq	%eax, %rdx	 # tmp113, tmp112
	movq	%rdx, %rax	 # tmp112, tmp114
	addq	%rax, %rax	 # tmp114
	addq	%rdx, %rax	 # tmp112, tmp114
	addq	%rcx, %rax	 # tmp110, tmp115
	movl	-48(%rbp,%rax,4), %eax	 # C[i_6][j_8], _1
	leaq	.LC1(%rip), %rcx	 #, tmp116
	movl	%eax, %edx	 # _1,
	call	printf	 #
 # matmul.c:59:         for (j = 0; j < N; j++)
	addl	$1, -8(%rbp)	 #, j
.L10:
 # matmul.c:59:         for (j = 0; j < N; j++)
	cmpl	$2, -8(%rbp)	 #, j
	jle	.L11	 #,
 # matmul.c:61:         printf("\n");
	movl	$10, %ecx	 #,
	call	putchar	 #
 # matmul.c:58:     for (i = 0; i < N; i++) {
	addl	$1, -4(%rbp)	 #, i
.L9:
 # matmul.c:58:     for (i = 0; i < N; i++) {
	cmpl	$2, -4(%rbp)	 #, i
	jle	.L12	 #,
 # matmul.c:64:     for (i = 0; i < N; i++)
	movl	$0, -4(%rbp)	 #, i
 # matmul.c:64:     for (i = 0; i < N; i++)
	jmp	.L13	 #
.L17:
 # matmul.c:65:         for (j = 0; j < N; j++)
	movl	$0, -8(%rbp)	 #, j
 # matmul.c:65:         for (j = 0; j < N; j++)
	jmp	.L14	 #
.L16:
 # matmul.c:66:             if (C[i][j] != EXPECTED[i][j]) {
	movl	-8(%rbp), %eax	 # j, tmp118
	movslq	%eax, %rcx	 # tmp118, tmp117
	movl	-4(%rbp), %eax	 # i, tmp120
	movslq	%eax, %rdx	 # tmp120, tmp119
	movq	%rdx, %rax	 # tmp119, tmp121
	addq	%rax, %rax	 # tmp121
	addq	%rdx, %rax	 # tmp119, tmp121
	addq	%rcx, %rax	 # tmp117, tmp122
	movl	-48(%rbp,%rax,4), %ecx	 # C[i_7][j_9], _2
 # matmul.c:66:             if (C[i][j] != EXPECTED[i][j]) {
	movl	-8(%rbp), %eax	 # j, tmp124
	movslq	%eax, %r8	 # tmp124, tmp123
	movl	-4(%rbp), %eax	 # i, tmp126
	movslq	%eax, %rdx	 # tmp126, tmp125
	movq	%rdx, %rax	 # tmp125, tmp127
	addq	%rax, %rax	 # tmp127
	addq	%rdx, %rax	 # tmp125, tmp127
	addq	%r8, %rax	 # tmp123, tmp128
	leaq	0(,%rax,4), %rdx	 #, tmp129
	leaq	EXPECTED(%rip), %rax	 #, tmp130
	movl	(%rdx,%rax), %eax	 # EXPECTED[i_7][j_9], _3
 # matmul.c:66:             if (C[i][j] != EXPECTED[i][j]) {
	cmpl	%eax, %ecx	 # _3, _2
	je	.L15	 #,
 # matmul.c:67:                 printf("MISMATCH [%d][%d]: got %d, want %d\n",
	movl	-8(%rbp), %eax	 # j, tmp132
	movslq	%eax, %rcx	 # tmp132, tmp131
	movl	-4(%rbp), %eax	 # i, tmp134
	movslq	%eax, %rdx	 # tmp134, tmp133
	movq	%rdx, %rax	 # tmp133, tmp135
	addq	%rax, %rax	 # tmp135
	addq	%rdx, %rax	 # tmp133, tmp135
	addq	%rcx, %rax	 # tmp131, tmp136
	leaq	0(,%rax,4), %rdx	 #, tmp137
	leaq	EXPECTED(%rip), %rax	 #, tmp138
	movl	(%rdx,%rax), %r8d	 # EXPECTED[i_7][j_9], _4
	movl	-8(%rbp), %eax	 # j, tmp140
	movslq	%eax, %rcx	 # tmp140, tmp139
	movl	-4(%rbp), %eax	 # i, tmp142
	movslq	%eax, %rdx	 # tmp142, tmp141
	movq	%rdx, %rax	 # tmp141, tmp143
	addq	%rax, %rax	 # tmp143
	addq	%rdx, %rax	 # tmp141, tmp143
	addq	%rcx, %rax	 # tmp139, tmp144
	movl	-48(%rbp,%rax,4), %r9d	 # C[i_7][j_9], _5
	movl	-8(%rbp), %edx	 # j, tmp145
	movl	-4(%rbp), %eax	 # i, tmp146
	leaq	.LC2(%rip), %rcx	 #, tmp147
	movl	%r8d, 32(%rsp)	 # _4,
	movl	%edx, %r8d	 # tmp145,
	movl	%eax, %edx	 # tmp146,
	call	printf	 #
 # matmul.c:69:                 fail = 1;
	movl	$1, -12(%rbp)	 #, fail
.L15:
 # matmul.c:65:         for (j = 0; j < N; j++)
	addl	$1, -8(%rbp)	 #, j
.L14:
 # matmul.c:65:         for (j = 0; j < N; j++)
	cmpl	$2, -8(%rbp)	 #, j
	jle	.L16	 #,
 # matmul.c:64:     for (i = 0; i < N; i++)
	addl	$1, -4(%rbp)	 #, i
.L13:
 # matmul.c:64:     for (i = 0; i < N; i++)
	cmpl	$2, -4(%rbp)	 #, i
	jle	.L17	 #,
 # matmul.c:72:     printf(fail ? "FAIL\n" : "OK: 9/9 elements match NumPy golden answer\n");
	cmpl	$0, -12(%rbp)	 #, fail
	je	.L18	 #,
 # matmul.c:72:     printf(fail ? "FAIL\n" : "OK: 9/9 elements match NumPy golden answer\n");
	leaq	.LC3(%rip), %rax	 #, iftmp.0_13
	jmp	.L19	 #
.L18:
 # matmul.c:72:     printf(fail ? "FAIL\n" : "OK: 9/9 elements match NumPy golden answer\n");
	leaq	.LC4(%rip), %rax	 #, iftmp.0_13
.L19:
 # matmul.c:72:     printf(fail ? "FAIL\n" : "OK: 9/9 elements match NumPy golden answer\n");
	movq	%rax, %rcx	 # iftmp.0_13,
	call	printf	 #
 # matmul.c:73:     return fail;
	movl	-12(%rbp), %eax	 # fail, _28
 # matmul.c:74: }
	addq	$96, %rsp	 #,
	popq	%rbp	 #
	ret	
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r3) 16.2.0"
	.def	puts;	.scl	2;	.type	32;	.endef
	.def	printf;	.scl	2;	.type	32;	.endef
	.def	putchar;	.scl	2;	.type	32;	.endef
