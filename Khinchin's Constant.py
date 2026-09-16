#!/usr/bin/env python3
"""
Khinchin's Constant Calculator (HPC OEIS Edition)
=================================================
Calculates Khinchin's constant (K_0) to exactly [N] significant digits using 
C-accelerated gmpy2 math and strict OEIS truncation formatting.
"""

import sys
import time
import argparse
import os

# Force mpmath to use gmpy2 for high-performance arbitrary-precision arithmetic
os.environ['MPMATH_GMPY2'] = '1'
import mpmath

# Allow printing/converting very large integers if supported
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def save_oeis_files(constant_name: str, digits_str: str, target_digits: int) -> None:
    """
    Saves the calculated digits of the constant to a raw text file and an OEIS b-file.

    Args:
        constant_name: The name of the constant (e.g., "Khinchin").
        digits_str: The string of digits (without decimal point).
        target_digits: The number of digits to save.
    """
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


def compute_khinchin_hpc(target_digits: int) -> str:
    """
    Computes Khinchin's constant to the target number of digits.

    Args:
        target_digits: The number of significant digits to compute.

    Returns:
        A string of the computed digits (without decimal point).
    """
    # Add guard digits to prevent trailing digit rounding errors
    dps_working = target_digits + 50
    mpmath.mp.dps = dps_working
    ctx = mpmath.mp

    khinchin_val = ctx.khinchin
    khinchin_str = ctx.nstr(khinchin_val, dps_working)
    clean_digits = khinchin_str.replace(".", "")[:target_digits]

    save_oeis_files("Khinchin", clean_digits, target_digits)
    return clean_digits


def main() -> None:
    """
    Main CLI entry point.
    """
    parser = argparse.ArgumentParser(description="HPC Khinchin OEIS Calculator")
    parser.add_argument("-n", "--digits", type=int, default=1000, help="Target digits (default: 1000)")
    args = parser.parse_args()

    t0 = time.time()
    _ = compute_khinchin_hpc(args.digits)
    t1 = time.time()

    print(f"Execution finished in {t1 - t0:.4f} seconds.")


if __name__ == "__main__":
    main()
