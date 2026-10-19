# NBA 9-Cat & 10-Cat Auction Draft Valuation Engine

**Author:** Harman Brah, MD

An exponential auction price-curve solver and interactive draft board for 9-category and 10-category fantasy basketball leagues ($300 budget, 9 or 10 teams, 15-player rosters).

## How It Works

1. **Exponential Budget Solver ([build_v2.py](build_v2.py)):** Uses binary search over an exponential decay curve (`1 + (top - 1) * exp(-i / k)`) so total auction values across all 135 or 150 roster spots sum to the exact league dollar pool (`$2,700` or `$3,000`).
2. **Role & Injury News Adjustments:** Layers preseason injury, trade, and usage adjustments onto base 9-category rankings, tagging players as Target (`T`), Fair Value (`V`), Avoid (`A`), or Out (`O`).
3. **10th-Category Dollar Nudges:** Computes explicit dollar adjustments when switching the 10th category between Double-Doubles (`DD`) and 3-Point Percentage (`3P%`).
4. **Interactive Auction Board ([gba-auction-board.html](gba-auction-board.html)):** Single-file browser board with live budget tracking, tier filtering, and category toggles.

## Quick Start

```bash
python3 build_v2.py
open gba-auction-board.html
```
