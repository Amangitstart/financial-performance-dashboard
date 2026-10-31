"""Run the whole pipeline:  python main.py  [--input path/to/file.csv]"""
import argparse
from pathlib import Path

from src import charts, config, dashboard, data_cleaning, metrics, report_pdf, report_word


def main():
    ap = argparse.ArgumentParser(description=config.PROJECT_TITLE)
    ap.add_argument("--input", type=Path, default=config.DEFAULT_INPUT, help="CSV or Excel file")
    args = ap.parse_args()

    print("1/5 Loading and cleaning data...")
    df, log = data_cleaning.clean(data_cleaning.load_raw(args.input))
    config.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(config.PROCESSED_DIR / "clean_data.csv", index=False)
    print(f"    {log['rows_raw']:,} raw rows -> {log['rows_clean']:,} clean rows "
          f"({log['duplicates_removed']} duplicates, {log['rows_missing_required']} missing, "
          f"{log['rows_negative_revenue']} negative revenue)")

    print("2/5 Calculating metrics...")
    m = metrics.build_all(df)
    m["yearly"].to_csv(config.PROCESSED_DIR / "yearly_summary.csv", index=False)
    for name in ("industry", "region", "top"):
        if m[name] is not None:
            m[name].to_csv(config.PROCESSED_DIR / f"{name}_summary.csv", index=False)

    print("3/5 Drawing charts...")
    chart_paths = charts.make_all(df, m)

    print("4/5 Building dashboard image...")
    dash = dashboard.build(df, m)

    print("5/5 Writing PDF and Word reports...")
    pdf = report_pdf.build(m, chart_paths, dash, log)
    docx = report_word.build(m, chart_paths, dash, log)

    print("\nDone. Key findings:")
    for line in m["insights"]:
        print(" -", line)
    print(f"\nDashboard: {dash}\nPDF:       {pdf}\nWord:      {docx}")


if __name__ == "__main__":
    main()
