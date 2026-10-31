"""Tiny self-contained tests. The data here is made up ONLY to check the code runs."""
import numpy as np
import pandas as pd
import pytest

from src import data_cleaning, metrics


def make_df():
    rng = np.random.default_rng(0)
    rows = []
    for cid in range(1, 21):
        for year in range(2015, 2019):
            rows.append({"CompanyID": cid, "Industry": "A" if cid % 2 else "B",
                         "Region": "X" if cid % 3 else "Y", "Year": year,
                         "Revenue": 1000 + rng.random() * 500,
                         "ProfitMargin": 10 + rng.random() * 5,
                         "ESG_Overall": 40 + rng.random() * 40})
    return pd.DataFrame(rows)


def test_clean_adds_net_profit_and_renames():
    df, log = data_cleaning.clean(make_df())
    assert "profit_margin" in df.columns and "net_profit" in df.columns
    assert np.allclose(df["net_profit"], df["revenue"] * df["profit_margin"] / 100)
    assert log["rows_clean"] == 80


def test_clean_drops_bad_rows():
    raw = make_df()
    raw.loc[0, "Revenue"] = None
    raw.loc[1, "Revenue"] = -5
    raw = pd.concat([raw, raw.iloc[[5]]])  # exact duplicate
    df, log = data_cleaning.clean(raw)
    assert log["duplicates_removed"] == 1
    assert log["rows_missing_required"] == 1
    assert log["rows_negative_revenue"] == 1


def test_fraction_margin_is_converted():
    raw = make_df()
    raw["ProfitMargin"] = raw["ProfitMargin"] / 100
    df, log = data_cleaning.clean(raw)
    assert log["margin_converted_from_fraction"] is True
    assert df["profit_margin"].max() > 5


def test_missing_required_column_raises():
    with pytest.raises(ValueError):
        data_cleaning.clean(make_df().drop(columns=["Revenue"]))


def test_metrics_shapes():
    df, _ = data_cleaning.clean(make_df())
    m = metrics.build_all(df)
    assert len(m["yearly"]) == 4
    assert m["kpis"]["companies"] == 20
    assert len(m["insights"]) >= 4
