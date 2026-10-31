# Financial Performance Dashboard

A Python project that cleans a company financial + ESG dataset, calculates key
performance numbers, draws a one-page dashboard, and writes **PDF** and **Word**
reports automatically. An optional Power BI / Excel version is included for an
interactive dashboard.

> Every number in the dashboard and reports is calculated from the dataset.
> Nothing is estimated, filled in, or invented. Rows with missing key values are dropped and counted.

## Tech stack

| Tool | Used for |
|---|---|
| Python (pandas, NumPy) | Data cleaning and calculations |
| Matplotlib | Charts and dashboard layout |
| ReportLab (PDF), python-docx (Word) | PDF and Word reports |
| Power BI / Excel (optional) | Interactive version of the dashboard |

## What you get

- `outputs/charts/00_dashboard.png` - one-page dashboard (KPI cards + 6 charts)
- `outputs/charts/01...06_*.png` - each chart on its own
- `outputs/reports/Financial_Performance_Report.pdf`
- `outputs/reports/Financial_Performance_Report.docx`
- `data/processed/*.csv` - cleaned data and summary tables (also used by Power BI)

## Project structure

```
financial-performance-dashboard/
├── main.py                  # run everything with one command
├── requirements.txt
├── README.md
├── LICENSE
├── data/
│   ├── raw/                 # put company_esg_financial_dataset.csv here
│   └── processed/           # cleaned CSVs are written here
├── src/
│   ├── config.py            # paths, colours, column-name aliases, currency unit
│   ├── utils.py             # number formatting helpers
│   ├── data_cleaning.py     # load, standardise, clean, add net_profit
│   ├── metrics.py           # yearly / industry / region / ESG numbers + insights
│   ├── charts.py            # Matplotlib charts
│   ├── dashboard.py         # one-page dashboard image
│   ├── report_pdf.py        # ReportLab PDF
│   └── report_word.py       # python-docx Word file
├── tests/test_pipeline.py   # pytest checks (uses tiny made-up data, only to test code)
├── powerbi/README.md        # steps + DAX measures for the interactive version
├── docs/                    # screenshots / extra notes
└── outputs/
    ├── charts/
    └── reports/
```

## How to run

```bash
git clone https://github.com/Amangitstart/financial-performance-dashboard.git
cd financial-performance-dashboard

python -m venv venv
venv\Scripts\activate          # Windows   (Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt

# 1. copy company_esg_financial_dataset.csv into data/raw/
# 2. run:
python main.py
# or with any file:
python main.py --input path/to/your_file.csv
```

Run the tests: `pytest`

## How the numbers are calculated

| Measure | Formula |
|---|---|
| Estimated net profit | `Revenue x Profit margin / 100` (per record) |
| Average revenue CAGR | `(avg revenue last year / avg revenue first year)^(1/years) - 1` |
| Weighted margin | `total net profit / total revenue` |
| Revenue growth | year-over-year change in average revenue per record |
| ESG vs margin | Pearson correlation (shows relationship, not cause) |

Revenue is assumed to be **USD million**. If your file uses another unit,
change `CURRENCY_UNIT` in `src/config.py` and the `fmt_money` helper in `src/utils.py`.

## Cleaning rules (all counted and printed when you run)

1. Column names are matched loosely (`ProfitMargin`, `Profit Margin`, `profit_margin` all work)
2. Exact duplicate rows removed
3. Rows missing year, revenue or profit margin removed
4. Rows with negative revenue removed
5. Profit margin converted to % if the file stores it as a fraction (0.15 -> 15)

## Optional: interactive Power BI version

See [`powerbi/README.md`](powerbi/README.md).

## Author

Aman - B.Tech Computer Science, ABES Engineering College
