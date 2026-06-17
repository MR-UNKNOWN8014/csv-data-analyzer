# CSV Data Analyzer

A Command line Python tool that loads any CSV file, computes detailed statistics on every numeric column, detects outliers using IQR & Z-Score, and exports a full summary report.

Built as a portfolio project while learning Python, Pandas, and NumPy.

---

## Features

- **Auto-detects all numeric columns**: no configuration needed
- **Descriptive statistics**: mean, median, std dev, min, max, Q1, Q3, IQR
- **Dual outlier detection:**
    - IQR method (box plot style, robust against skewed data)
    - Z-Score method (standard deviation based)
- **Colored terminal report**: ANSI-styled, easy to read at a glance
- **Exports timestamped `.txt` report**: saved automatically next to your CSV
- **Flexible input**: pass CSV path as a CLI argument or get prompted interactively

---

## Demo

```
python csv_analyzer.py employees.csv
```

```
════════════════════════════════════════════════════════════
  📁 FILE OVERVIEW
════════════════════════════════════════════════════════════
  File     : employees.csv
  Rows     : 206
  Columns  : 8
  Numeric  : 7

════════════════════════════════════════════════════════════
  📊 COLUMN: Salary
════════════════════════════════════════════════════════════
  Count              206
  Mean               63,412.0
  Median             60,250.0
  Std Dev            34,201.0
  Min                46,000.0
  Max                500,000.0
  Q1                 52,000.0
  Q3                 72,000.0
  IQR                20,000.0

  ▶ IQR Outliers  (fence: 22000.0 → 102000.0)
    Count : 2
    Values: [200000, 500000]

  ▶ Z-Score Outliers  (|z| > 3)
    Count : 1
    Values: [500000]
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/MR-UNKNOWN8014/csv-data-analyzer.git
cd csv-data-analyzer
```

### 2. Install dependencies

```bash
pip install pandas numpy
```

### 3. Run the analyzer

```bash
# Option A — pass the file directly
python csv_analyzer.py your_file.csv

# Option B — get prompted
python csv_analyzer.py
```

---

## Project Structure

```
csv-data-analyzer/
│
├── csv_analyzer.py          # Main script
├── employees_sample.csv     # Sample dataset for testing (with planted outliers)
├── requirements.txt         # Dependencies
├── .gitignore
└── README.md
```

---

## Requirements

```
pandas
numpy
```

Or install directly:

```bash
pip install -r requirements.txt
```

---

## Testing with Sample Data

A sample dataset `employees_sample.csv` is included with **planted outliers** so you can immediately verify the analyzer is working:

---

## Concepts Demonstrated

- Pandas DataFrames and Series
- NumPy statistical functions
- IQR-based outlier detection
- Z-Score outlier detection
- `argparse` for CLI argument handling
- File I/O with UTF-8 encoding
- ANSI terminal colors
- Modular function design


---
