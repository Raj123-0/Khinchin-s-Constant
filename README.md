[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

===============================================================================
PROJECT: Khinchin's Constant Computation Engine
===============================================================================

OVERVIEW:
Calculates Khinchin's constant (K_0 ≈ 2.68545200106530644143...) to arbitrary 
precision (N digits). Khinchin proved that for almost all real numbers, the 
geometric mean of the continued fraction terms converges to K_0.

ALGORITHM & MATHEMATICS:
- Riemann Zeta Expansion:
    ln(K_0) = (1 / ln 2) * sum_{n=1}^{infinity} ((zeta(2n) - 1) / n) * sum_{k=1}^{2n-1} ((-1)^(k+1) / k)
- Fast Series Acceleration using gmpy2 and mpmath context guards.

## Usage

```bash
python "Khinchin's Constant.py" --help
```
