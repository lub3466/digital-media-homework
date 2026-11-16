// dot.rs — Rust 版点积（仅标准库，--release / -C opt-level=2 编译）
//
// 用法：dot_rs.exe <a.bin> <b.bin> <n>
//
// 计时协议与 Python / C 完全一致：读文件不计时；预热 10 轮后正式
// 200 轮，同时输出最小值与中位数；每轮结果累加进 checksum 并被
// println! 消费，防止编译器把整段循环优化成常量。

use std::convert::TryInto;
use std::env;
use std::fs::File;
use std::io::Read;
use std::time::Instant;

const WARMUP: usize = 10;
const ROUNDS: usize = 200;

fn read_f64(path: &str) -> Vec<f64> {
    let mut f = File::open(path).expect("open failed");
    let mut raw = Vec::new();
    f.read_to_end(&mut raw).expect("read failed");
    raw.chunks_exact(8)
        .map(|c| f64::from_le_bytes(c.try_into().unwrap()))
        .collect()
}

fn dot(a: &[f64], b: &[f64]) -> f64 {
    a.iter().zip(b.iter()).map(|(x, y)| x * y).sum()
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 4 {
        eprintln!("usage: dot_rs <a.bin> <b.bin> <n>");
        std::process::exit(2);
    }
    let a = read_f64(&args[1]);
    let b = read_f64(&args[2]);
    let n: usize = args[3].parse().expect("bad n");
    assert_eq!(a.len(), n, "length mismatch a");
    assert_eq!(b.len(), n, "length mismatch b");

    // checksum 被 println! 消费，编译器无法证明它是死代码
    let mut checksum = 0.0f64;
    for _ in 0..WARMUP {
        checksum += dot(&a, &b);
    }

    let mut times = [0.0f64; ROUNDS];
    for slot in times.iter_mut() {
        let t0 = Instant::now();
        checksum += dot(&a, &b);
        *slot = t0.elapsed().as_secs_f64();
    }

    times.sort_by(|x, y| x.partial_cmp(y).unwrap());
    let median = (times[ROUNDS / 2] + times[(ROUNDS - 1) / 2]) / 2.0;
    let minimum = times[0]; // 排序后第一个即最小值

    let result = dot(&a, &b);
    println!(
        "lang=rust n={} result={:.12} checksum={:.6} median_us={:.2} min_us={:.2}",
        n, result, checksum, median * 1e6, minimum * 1e6
    );
}
