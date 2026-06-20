import pandas as pd
import numpy as np
import argparse
import os
from datetime import datetime

CYAN    = "\033[96m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
RED     = "\033[91m"
BOLD    = "\033[1m"
RESET   = "\033[0m"

# Separator Helpers
def divider(char="=", width=60):
    return char * width

def section(title):
    print(f"\n{CYAN}{BOLD}{divider()}{RESET}")
    print(f"{CYAN}{BOLD}  {title}{RESET}")
    print(f"{CYAN}{divider()}{RESET}")


# Load CSV
def load_csv(filepath):
    """Function to load a csv file into a pandas dataframe"""
    if not os.path.exists(filepath):
        print(f"{RED}ERROR: File not found → {filepath}{RESET}")
        exit(1)
    if not filepath.endswith(".csv"):
        print(f"{YELLOW}WARNING: File may not be a CSV → {filepath}{RESET}")

    df = pd.read_csv(filepath)
    print(f"\n{GREEN} Loaded:{RESET} {filepath}")
    print(f"  Rows: {df.shape[0]}  |  Columns: {df.shape[1]}")
    return df


# Identify Numeric Columns
def get_numeric_columns(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric_cols:
        print(f"{RED}No numeric columns found. Exiting.{RESET}")
        exit(1)
    return numeric_cols


# Compute Statistics for one Column
def compute_stats(series):
    """
        Given a Pandas Series (one column of numbers),
        compute and return a dict of statistics.
    """
    stats = {
        "count": int(series.count()),
        "missing": int(series.isna().sum()),
        "mean": round(float(series.mean()), 4),
        "median": round(float(series.median()), 4),
        "std": round(float(series.std()), 4),
        "min": round(float(series.min()), 4),
        "max": round(float(series.max()), 4),
        "q1": round(float(series.quantile(0.25)), 4),
        "q3": round(float(series.quantile(0.75)), 4),
    }
    stats["iqr"] = round(stats["q3"] - stats["q1"], 4)
    return stats


# Detect Outliers (IQR + Z-Score)
def detect_outliers(series, stats):
    """
        Detect outliers using two methods:
          - IQR  -> values outside Q1-1.5*IQR  or  Q3+1.5*IQR
          - Z-Score -> values where |z| > 3
        Returns two lists of outlier values.
    """
    clean = series.dropna() # remove NaN before calculations

    # IQR Method
    lower_fence = stats["q1"] - 1.5 * stats["iqr"]
    upper_fence = stats["q3"] + 1.5 * stats["iqr"]
    iqr_outliers = clean[(clean < lower_fence) | (clean > upper_fence)].tolist()

    # Z-Score Method
    z_scores = np.abs((clean - clean.mean()) / clean.std())
    zscore_outliers = clean[z_scores > 3].tolist()

    return (
        sorted(iqr_outliers),
        sorted(zscore_outliers),
        round(lower_fence, 4),
        round(upper_fence, 4),
    )


# Print Terminal Report
def print_report(df, numeric_cols, all_stats, all_outliers, filepath):
    section("FILE OVERVIEW")
    print(f"  File     : {filepath}")
    print(f"  Rows     : {df.shape[0]}")
    print(f"  Columns  : {df.shape[1]}")
    print(f"  Numeric  : {len(numeric_cols)}")
    print(f"  Non-Num  : {df.shape[1] - len(numeric_cols)}")
    print(f"  All cols : {list(df.columns)}")

    for col in numeric_cols:
        s = all_stats[col]
        iqr_out, z_out, low_f, high_f = all_outliers[col]

        section(f"COLUMN: {col}")
        print(f"  {'Count':<18} {s['count']}")
        print(f"  {'Missing':<18} {s['missing']}")
        print(f"  {'Mean':<18} {s['mean']}")
        print(f"  {'Median':<18} {s['median']}")
        print(f"  {'Std Dev':<18} {s['std']}")
        print(f"  {'Min':<18} {s['min']}")
        print(f"  {'Max':<18} {s['max']}")
        print(f"  {'Q1 (25%)':<18} {s['q1']}")
        print(f"  {'Q3 (75%)':<18} {s['q3']}")
        print(f"  {'IQR':<18} {s['iqr']}")

        # IQR Outliers
        print(f"\n  {YELLOW} IQR Outliers{RESET}  (fence: {low_f} -> {high_f})")
        if iqr_out:
            print(f"  {RED}  Count : {len(iqr_out)}{RESET}")
            print(f"    Values: {iqr_out[:20]}{'...' if len(iqr_out) > 20 else ''}")
        else:
            print(f"  {GREEN}  None detected{RESET}")

        # Z-Score Outliers
        print(f"\n  {YELLOW} Z-Score Outliers{RESET}  (|z| > 3)")
        if z_out:
            print(f"  {RED}  Count : {len(z_out)}{RESET}")
            print(f"    Values: {z_out[:20]}{'...' if len(z_out) > 20 else ''}")
        else:
            print(f"  {GREEN}  None detected{RESET}")

    print(f"\n{CYAN}{divider()}{RESET}\n")


# Export Report to a TXT File
def export_report(df, numeric_cols, all_stats, all_outliers, filepath):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    output_file = f"{base_name}_report_{timestamp}.txt"

    lines = []
    lines.append("=" * 60)
    lines.append("  CSV DATA ANALYSIS REPORT")
    lines.append(f"  Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"  File      : {filepath}")
    lines.append("=" * 60)
    lines.append(f"\nRows     : {df.shape[0]}")
    lines.append(f"Columns  : {df.shape[1]}")
    lines.append(f"Numeric  : {len(numeric_cols)}")
    lines.append(f"All cols : {list(df.columns)}\n")

    for col in numeric_cols:
        s = all_stats[col]
        iqr_out, z_out, low_f, high_f = all_outliers[col]

        lines.append("-" * 60)
        lines.append(f"COLUMN: {col}")
        lines.append("-" * 60)
        lines.append(f"  Count          : {s['count']}")
        lines.append(f"  Missing        : {s['missing']}")
        lines.append(f"  Mean           : {s['mean']}")
        lines.append(f"  Median         : {s['median']}")
        lines.append(f"  Std Dev        : {s['std']}")
        lines.append(f"  Min            : {s['min']}")
        lines.append(f"  Max            : {s['max']}")
        lines.append(f"  Q1 (25%)       : {s['q1']}")
        lines.append(f"  Q3 (75%)       : {s['q3']}")
        lines.append(f"  IQR            : {s['iqr']}")
        lines.append(f"\n  IQR Outliers   (fence: {low_f} → {high_f})")
        lines.append(f"    Count  : {len(iqr_out)}")
        lines.append(f"    Values : {iqr_out[:20]}{'...' if len(iqr_out) > 20 else ''}")
        lines.append(f"\n  Z-Score Outliers (|z| > 3)")
        lines.append(f"    Count  : {len(z_out)}")
        lines.append(f"    Values : {z_out[:20]}{'...' if len(z_out) > 20 else ''}")
        lines.append("")

    lines.append("=" * 60)
    lines.append("  END OF REPORT")
    lines.append("=" * 60)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"{GREEN}✔ Report saved →{RESET} {output_file}\n")
    return output_file

# Export Report to a JSON File
def export_json(df, numeric_cols, all_stats, all_outliers, filepath):
    import json

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    output_file = f"{base_name}_report_{timestamp}.json"

    report = {
        "generated": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "file": filepath,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "all_columns": list(df.columns),
        "numeric_columns": {}
    }

    for col in numeric_cols:
        s = all_stats[col]
        iqr_out, z_out, low_f, high_f = all_outliers[col]

        report["numeric_columns"][col] = {
            "stats": s,
            "iqr_outliers": {
                "fence_low": low_f,
                "fence_high": high_f,
                "count": len(iqr_out),
                "values": iqr_out
            },
            "zscore_outliers": {
                "count": len(z_out),
                "values": z_out
            }
        }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"{GREEN}✔ Report saved →{RESET} {output_file}\n")
    return output_file


# Export Report to a CSV File
def export_csv(df, numeric_cols, all_stats, all_outliers, filepath):
    import csv

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    output_file = f"{base_name}_report_{timestamp}.csv"

    fieldnames = [
        "column", "count", "missing", "mean", "median", "std",
        "min", "max", "q1", "q3", "iqr",
        "iqr_outlier_count", 'zscore_outlier_count'
    ]

    with open(output_file, "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for col in numeric_cols:
            s = all_stats[col]
            iqr_out, z_out, low_f, high_f = all_outliers[col]

            row = dict(s)
            row["column"] = col
            row["iqr_outlier_count"] = len(iqr_out)
            row["zscore_outlier_count"] = len(z_out)
            writer.writerow(row)

    print(f"{GREEN}✔ Report saved →{RESET} {output_file}\n")
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description="CSV Data Analyzer: stats, outliers, and report"
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to the CSV file"
    )
    parser.add_argument(
        "--export",
        choices=["txt", "json", "csv"],
        help="Export report format: txt, json, or csv"
    )
    args = parser.parse_args()

    # Terminal Prompt
    if args.file:
        filepath = args.file
    else:
        filepath = input("Please enter the file path: ").strip()

    df = load_csv(filepath)
    numeric_cols = get_numeric_columns(df)

    all_stats = {}
    all_outliers = {}

    for col in numeric_cols:
        series = df[col]
        all_stats[col] = compute_stats(series)
        all_outliers[col] = detect_outliers(series, all_stats[col])

    print_report(df, numeric_cols, all_stats, all_outliers, filepath)

    if args.export == "txt":
        export_report(df, numeric_cols, all_stats, all_outliers, filepath)
    elif args.export == "json":
        export_json(df, numeric_cols, all_stats, all_outliers, filepath)
    elif args.export == "csv":
        export_csv(df, numeric_cols, all_stats, all_outliers, filepath)

if __name__ == "__main__":
    main()