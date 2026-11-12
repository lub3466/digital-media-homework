	.file	"matmul.c"
 # GNU C23 (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r3) version 16.2.0 (x86_64-w64-mingw32)
 #	compiled by GNU C version 16.2.0, GMP version 6.3.0, MPFR version 4.2.2, MPC version 1.4.1, isl version isl-0.28-GMP

 # GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
 # options passed: -mtune=generic -march=x86-64 -O2
	.text
	.p2align 4
	.globl	matmul
	.def	matmul;	.scl	2;	.type	32;	.endef
	.seh_proc	matmul
matmul:
	.seh_endprologue
 # matmul.c:36: {
	movq	%rdx, %r10	 # b, b
	leaq	36(%rcx), %r11	 #, _47
.L2:
 # matmul.c:44:             c[i][j] = s;
	xorl	%eax, %eax	 # ivtmp.17
.L3:
 # matmul.c:42:                 s += a[i][k] * b[k][j];   /* 最内层的乘加 */
	movl	(%r10,%rax), %r9d	 # MEM[(int *)b_25(D) + ivtmp.17_28 * 1], MEM[(int *)b_25(D) + ivtmp.17_28 * 1]
 # matmul.c:42:                 s += a[i][k] * b[k][j];   /* 最内层的乘加 */
	movl	4(%rcx), %edx	 # MEM[(int *)_48 + 4B], MEM[(int *)_48 + 4B]
 # matmul.c:42:                 s += a[i][k] * b[k][j];   /* 最内层的乘加 */
	imull	(%rcx), %r9d	 # MEM[(int *)_48], _13
 # matmul.c:42:                 s += a[i][k] * b[k][j];   /* 最内层的乘加 */
	imull	12(%r10,%rax), %edx	 # MEM[(int *)b_25(D) + 12B + ivtmp.17_28 * 1], _55
 # matmul.c:42:                 s += a[i][k] * b[k][j];   /* 最内层的乘加 */
	addl	%edx, %r9d	 # _55, s
 # matmul.c:42:                 s += a[i][k] * b[k][j];   /* 最内层的乘加 */
	movl	8(%rcx), %edx	 # MEM[(int *)_48 + 8B], MEM[(int *)_48 + 8B]
	imull	24(%r10,%rax), %edx	 # MEM[(int *)b_25(D) + 24B + ivtmp.17_28 * 1], _9
 # matmul.c:42:                 s += a[i][k] * b[k][j];   /* 最内层的乘加 */
	addl	%r9d, %edx	 # s, tmp124
	movl	%edx, (%r8,%rax)	 # tmp124, MEM[(int *)_12 + ivtmp.17_28 * 1]
 # matmul.c:39:         for (j = 0; j < N; j++) {
	addq	$4, %rax	 #, ivtmp.17
	cmpq	$12, %rax	 #, ivtmp.17
	jne	.L3	 #,
 # matmul.c:38:     for (i = 0; i < N; i++) {
	addq	$12, %rcx	 #, ivtmp.25
	addq	$12, %r8	 #, ivtmp.26
	cmpq	%r11, %rcx	 # _47, ivtmp.25
	jne	.L2	 #,
 # matmul.c:47: }
	ret	
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "FAIL\12\0"
	.align 8
.LC1:
	.ascii "OK: 9/9 elements match NumPy golden answer\12\0"
.LC2:
	.ascii "C = A x B :\0"
.LC3:
	.ascii "%4d \0"
	.align 8
.LC4:
	.ascii "MISMATCH [%d][%d]: got %d, want %d\12\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
	pushq	%r12	 #
	.seh_pushreg	%r12
	pushq	%rbp	 #
	.seh_pushreg	%rbp
	pushq	%rdi	 #
	.seh_pushreg	%rdi
	pushq	%rsi	 #
	.seh_pushreg	%rsi
	pushq	%rbx	 #
	.seh_pushreg	%rbx
	subq	$96, %rsp	 #,
	.seh_stackalloc	96
	.seh_endprologue
 # matmul.c:50: {
	call	__main	 #
 # matmul.c:55:     matmul(A, B, C);
	leaq	48(%rsp), %r8	 #, tmp139
	leaq	48(%rsp), %rsi	 #, tmp140
	leaq	B(%rip), %rdx	 #,
	leaq	A(%rip), %rcx	 #,
 # matmul.c:57:     printf("C = A x B :\n");
	movq	%rsi, %rdi	 # ivtmp.50, ivtmp.66
 # matmul.c:55:     matmul(A, B, C);
	call	matmul	 #
 # matmul.c:57:     printf("C = A x B :\n");
	leaq	.LC2(%rip), %rcx	 #,
	leaq	84(%rsp), %rbp	 #, _71
	call	puts	 #
.L8:
 # matmul.c:50: {
	xorl	%ebx, %ebx	 # ivtmp.54
.L9:
 # matmul.c:60:             printf("%4d ", C[i][j]);
	movl	(%rdi,%rbx,4), %edx	 # MEM[(int *)_66 + ivtmp.54_60 * 4], MEM[(int *)_66 + ivtmp.54_60 * 4]
	leaq	.LC3(%rip), %rcx	 #,
 # matmul.c:59:         for (j = 0; j < N; j++)
	addq	$1, %rbx	 #, ivtmp.54
 # matmul.c:60:             printf("%4d ", C[i][j]);
	call	printf	 #
 # matmul.c:59:         for (j = 0; j < N; j++)
	cmpq	$3, %rbx	 #, ivtmp.54
	jne	.L9	 #,
 # matmul.c:61:         printf("\n");
	movl	$10, %ecx	 #,
 # matmul.c:58:     for (i = 0; i < N; i++) {
	addq	$12, %rdi	 #, ivtmp.66
 # matmul.c:61:         printf("\n");
	call	putchar	 #
 # matmul.c:58:     for (i = 0; i < N; i++) {
	cmpq	%rbp, %rdi	 # _71, ivtmp.66
	jne	.L8	 #,
	leaq	EXPECTED(%rip), %rdi	 #, ivtmp.51
 # matmul.c:53:     int fail = 0;
	xorl	%r12d, %r12d	 # <retval>
 # matmul.c:64:     for (i = 0; i < N; i++)
	xorl	%ebp, %ebp	 # i
.L10:
 # matmul.c:57:     printf("C = A x B :\n");
	xorl	%ebx, %ebx	 # ivtmp.36
.L12:
 # matmul.c:66:             if (C[i][j] != EXPECTED[i][j]) {
	movl	(%rsi,%rbx,4), %r9d	 # MEM[(int *)_37 + ivtmp.36_7 * 4], _2
 # matmul.c:66:             if (C[i][j] != EXPECTED[i][j]) {
	movl	(%rdi,%rbx,4), %eax	 # MEM[(int *)_31 + ivtmp.36_7 * 4], _3
 # matmul.c:66:             if (C[i][j] != EXPECTED[i][j]) {
	cmpl	%eax, %r9d	 # _3, _2
	je	.L11	 #,
 # matmul.c:67:                 printf("MISMATCH [%d][%d]: got %d, want %d\n",
	movl	%eax, 32(%rsp)	 # _3,
	movl	%ebx, %r8d	 # ivtmp.36,
	movl	%ebp, %edx	 # i,
	leaq	.LC4(%rip), %rcx	 #,
 # matmul.c:69:                 fail = 1;
	movl	$1, %r12d	 #, <retval>
 # matmul.c:67:                 printf("MISMATCH [%d][%d]: got %d, want %d\n",
	call	printf	 #
.L11:
 # matmul.c:65:         for (j = 0; j < N; j++)
	addq	$1, %rbx	 #, ivtmp.36
	cmpq	$3, %rbx	 #, ivtmp.36
	jne	.L12	 #,
 # matmul.c:64:     for (i = 0; i < N; i++)
	addl	$1, %ebp	 #, i
 # matmul.c:64:     for (i = 0; i < N; i++)
	addq	$12, %rsi	 #, ivtmp.50
	addq	$12, %rdi	 #, ivtmp.51
	cmpl	$3, %ebp	 #, i
	jne	.L10	 #,
 # matmul.c:72:     printf(fail ? "FAIL\n" : "OK: 9/9 elements match NumPy golden answer\n");
	testl	%r12d, %r12d	 # <retval>
	leaq	.LC0(%rip), %rax	 #, tmp133
 # matmul.c:72:     printf(fail ? "FAIL\n" : "OK: 9/9 elements match NumPy golden answer\n");
	leaq	.LC1(%rip), %rcx	 #, iftmp.0_11
 # matmul.c:72:     printf(fail ? "FAIL\n" : "OK: 9/9 elements match NumPy golden answer\n");
	cmovne	%rax, %rcx	 # iftmp.0_11,, tmp133, iftmp.0_11
 # matmul.c:72:     printf(fail ? "FAIL\n" : "OK: 9/9 elements match NumPy golden answer\n");
	call	printf	 #
 # matmul.c:74: }
	movl	%r12d, %eax	 # <retval>,
	addq	$96, %rsp	 #,
	popq	%rbx	 #
	popq	%rsi	 #
	popq	%rdi	 #
	popq	%rbp	 #
	popq	%r12	 #
	ret	
	.seh_endproc
	.section .rdata,"dr"
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
	.data
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
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (MinGW-W64 x86_64-ucrt-posix-seh, built by Brecht Sanders, r3) 16.2.0"
	.def	puts;	.scl	2;	.type	32;	.endef
	.def	printf;	.scl	2;	.type	32;	.endef
	.def	putchar;	.scl	2;	.type	32;	.endef
