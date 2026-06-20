# CSV Data Analyzer

A command-line Python tool that loads any CSV file, computes detailed statistics on every numeric column, detects outliers using IQR & Z-Score methods, and exports comprehensive reports in multiple formats.

Built as a portfolio project while learning Python, Pandas, NumPy, and data analysis workflows.

---

## Features

- **Auto-detects all numeric columns**: no configuration needed
- **Descriptive statistics**: mean, median, std dev, min, max, Q1, Q3, IQR
- **Dual outlier detection:**
  - IQR method (box plot style, robust against skewed data)
  - Z-Score method (standard deviation based, flags extreme outliers)
- **Colored terminal report**: ANSI-styled output, easy to scan at a glance
- **Multi-format exports**: save reports as `.txt`, `.json`, or `.csv`
- **Flexible input**: pass CSV path as CLI argument or get prompted interactively
- **Optional exports**: terminal report always displays; file export only runs when `--export` flag is specified

---

## Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/MR-UNKNOWN8014/csv-data-analyzer.git
cd csv-data-analyzer
pip install -r requirements.txt
```

### 2. Run the analyzer
```bash
# Terminal report only
python csv_analyzer.py employees.csv

# Export as JSON
python csv_analyzer.py employees.csv --export json

# Export as CSV
python csv_analyzer.py employees.csv --export csv

# Export as TXT
python csv_analyzer.py employees.csv --export txt

# Get prompted for filename
python csv_analyzer.py
```

---

## Usage

| Command | Output |
|---------|--------|
| `python csv_analyzer.py data.csv` | Displays terminal report only |
| `python csv_analyzer.py data.csv --export txt` | Terminal report + timestamped `.txt` file |
| `python csv_analyzer.py data.csv --export json` | Terminal report + structured `.json` file |
| `python csv_analyzer.py data.csv --export csv` | Terminal report + flat `.csv` file |

---

## Example Output
```
════════════════════════════════════════════════════════════

FILE OVERVIEW

════════════════════════════════════════════════════════════

File     : employees.csv

Rows     : 206

Columns  : 8

Numeric  : 7

All cols : ['Name', 'Department', 'Salary', 'Age', 'Experience', 'Bonus', 'Score']
════════════════════════════════════════════════════════════

COLUMN: Salary

════════════════════════════════════════════════════════════

Count                  206

Missing                0

Mean                   63412.0

Median                 60250.0

Std Dev                34201.0

Min                    46000.0

Max                    500000.0

Q1 (25%)               52000.0

Q3 (75%)               72000.0

IQR                    20000.0
IQR Outliers  (fence: 22000.0 → 102000.0)

Count : 2

Values: [200000, 500000]
Z-Score Outliers  (|z| > 3)

Count : 1

Values: [500000]
```
---

## Project Structure
```bash
csv-data-analyzer/
│
├── csv_analyzer.py          # Main script
├── requirements.txt         # Dependencies
├── .gitignore
└── README.md
```
---

## Requirements
pandas & numpy

**Install with**:
```bash
pip install -r requirements.txt
```

---

## How It Works

### Statistics Computed
- **Count**: number of non-null values
- **Missing**: number of null/NaN values
- **Mean, Median, Std Dev**: central tendency and spread
- **Min, Max**: range of values
- **Q1, Q3, IQR**: quartile-based distribution metrics

### Outlier Detection Methods

1. **IQR Method (Interquartile Range):**
- Calculates fence: Q1 - 1.5×IQR to Q3 + 1.5×IQR
- Robust against skewed distributions
- Standard in exploratory data analysis

2. **Z-Score Method:**
- Flags values beyond 3 standard deviations from mean
- Detects more extreme outliers
- Assumes roughly normal distribution

---

## Concepts Demonstrated

- **Data Analysis**: Pandas DataFrames, Series operations, statistical functions
- **Numerical Computing**: NumPy array operations, quantile calculations
- **Statistical Methods**: IQR and Z-Score outlier detection
- **CLI Design**: `argparse` for flexible command-line arguments
- **File I/O**: Reading CSV files, writing multiple export formats
- **Data Serialization**: JSON encoding, CSV writing with proper type conversion
- **Terminal UI**: ANSI color codes for readable colored output
- **Modular Design**: Separated concerns across functions (load, compute, report, export)
- **Error Handling**: File validation, missing data checks, type conversion
