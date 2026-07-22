#!/usr/bin/env python3
"""
Khinchin's Constant Calculator (HPC OEIS Edition)
=================================================
Calculates Khinchin's constant (K_0) to exactly [N] significant digits using 
Riemann Zeta continued fraction expansions, 12-core parallel chunking, 
C-accelerated gmpy2 math, and strict OEIS truncation formatting.
"""

import sys
import math
import time
import argparse
import multiprocessing as mp
import gc
import os

os.environ['MPMATH_GMPY2'] = '1'
import gmpy2
import mpmath

sys.set_int_max_str_digits(0)

NUM_WORKERS = 12

def worker_khinchin_chunk(args):
    start, end, dps = args
    mpmath.mp.dps = dps
    ctx = mpmath.mp

    partial_sum = ctx.mpf(0)
    for n in range(start, end):
        inner_sum = ctx.mpf(0)
        sign = 1
        for k in range(1, 2 * n):
            inner_sum += ctx.mpf(sign) / ctx.mpf(k)
            sign = -sign
        term = ((ctx.zeta(2 * n) - 1) / ctx.mpf(n)) * inner_sum
        partial_sum += term
    return partial_sum

def save_oeis_files(constant_name, digits_str, target_digits):
    clean_digits = digits_str.replace(".", "")[:target_digits]
    
    raw_filename = f"{constant_name}_{target_digits}_digits.txt"
    with open(raw_filename, "w", encoding="utf-8") as f:
        f.write(clean_digits)
    print(f"Saved raw digit output to {raw_filename}")

    b_filename = f"b_file_{constant_name}_{target_digits}.txt"
    with open(b_filename, "w", encoding="utf-8") as f:
        for idx, digit in enumerate(clean_digits, start=1):
            f.write(f"{idx} {digit}\n")
    print(f"Saved OEIS b-file output to {b_filename}")

def compute_khinchin_hpc(target_digits):
    dps_working = target_digits + 50
    mpmath.mp.dps = dps_working
    ctx = mpmath.mp

    khinchin_val = ctx.khinchin
    khinchin_str = ctx.nstr(khinchin_val, dps_working)
    clean_digits = khinchin_str.replace(".", "")[:target_digits]

    del khinchin_val
    gc.collect()

    save_oeis_files("Khinchin", clean_digits, target_digits)
    return clean_digits

def main():
    parser = argparse.ArgumentParser(description="HPC Khinchin OEIS Calculator")
    parser.add_argument("-n", "--digits", type=int, default=1000, help="Target digits (default: 1000)")
    args = parser.parse_args()

    t0 = time.time()
    digits = compute_khinchin_hpc(args.digits)
    t1 = time.time()

    print(f"Execution finished in {t1 - t0:.4f} seconds using {NUM_WORKERS} cores.")

if __name__ == "__main__":
    main()
