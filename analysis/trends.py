import pandas as pd


def sales_by_week(df: pd.DataFrame) -> pd.DataFrame:
    """Return total revenue grouped by week."""
    # Ensure InvoiceDate is datetime (day-first format) before resampling
    df2 = df.copy()
    df2["InvoiceDate"] = pd.to_datetime(df2["InvoiceDate"], dayfirst=True, errors="coerce")
    df2 = df2.dropna(subset=["InvoiceDate"]) 
    return (
        df2.resample("W", on="InvoiceDate")["Revenue"]
        .sum()
        .reset_index()
        .rename(columns={"Revenue": "WeeklyRevenue"})
    )


def sales_growth(df: pd.DataFrame) -> dict:
    """Compare the most recent week's revenue to the previous week."""
    weekly = sales_by_week(df)

    if len(weekly) < 2:
        return {"current": 0, "previous": 0, "growth_pct": 0}

    current = weekly.iloc[-1]["WeeklyRevenue"]
    previous = weekly.iloc[-2]["WeeklyRevenue"]
    growth_pct = ((current - previous) / previous * 100) if previous else 0

    return {
        "current": round(current, 2),
        "previous": round(previous, 2),
        "growth_pct": round(growth_pct, 1),
    }


def country_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Return revenue totals ranked by country."""
    return (
        df.groupby("Country")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"Revenue": "TotalRevenue"})
    )


def sales_growth_multi(df: pd.DataFrame) -> dict:
    """Return growth comparisons for last week, last year (same week), and last quarter.

    Returns a dict with keys `week`, `year`, and `quarter`. Each value is a dict
    with `current`, `previous`, and `growth_pct`.
    """
    weekly = sales_by_week(df)

    # Prepare defaults
    def _entry(curr: float, prev: float) -> dict:
        # Compute percentage change. When previous is zero:
        # - if both current and previous are zero => 0%
        # - if previous is zero and current > 0 => show 100% to indicate new growth
        if prev:
            pct = (curr - prev) / prev * 100
        else:
            if curr:
                pct = 100.0
            else:
                pct = 0.0
        return {
            "current": round(float(curr), 2),
            "previous": round(float(prev), 2),
            "growth_pct": round(float(pct), 1),
        }

    # Week-over-week
    if len(weekly) >= 1:
        current_week_rev = weekly.iloc[-1]["WeeklyRevenue"]
    else:
        current_week_rev = 0.0

    if len(weekly) >= 2:
        prev_week_rev = weekly.iloc[-2]["WeeklyRevenue"]
    else:
        prev_week_rev = 0.0

    week_entry = _entry(current_week_rev, prev_week_rev)

    # Month-over-month: aggregate by calendar month and compare last two months
    # Use month-end offset 'ME' for compatibility with newer pandas versions
    monthly = (
        df.resample("ME", on="InvoiceDate")["Revenue"]
        .sum()
        .reset_index()
        .rename(columns={"Revenue": "MonthlyRevenue"})
    )

    if len(monthly) >= 1:
        current_month_rev = monthly.iloc[-1]["MonthlyRevenue"]
    else:
        current_month_rev = 0.0

    if len(monthly) >= 2:
        prev_month_rev = monthly.iloc[-2]["MonthlyRevenue"]
    else:
        prev_month_rev = 0.0

    month_entry = _entry(current_month_rev, prev_month_rev)

    # Quarter-over-quarter: aggregate by calendar quarter
    # Use quarter-end offset 'QE' for compatibility with newer pandas versions
    quarterly = (
        df.resample("QE", on="InvoiceDate")["Revenue"]
        .sum()
        .reset_index()
        .rename(columns={"Revenue": "QuarterlyRevenue"})
    )

    if len(quarterly) >= 1:
        current_q_rev = quarterly.iloc[-1]["QuarterlyRevenue"]
    else:
        current_q_rev = 0.0

    if len(quarterly) >= 2:
        prev_q_rev = quarterly.iloc[-2]["QuarterlyRevenue"]
    else:
        prev_q_rev = 0.0

    quarter_entry = _entry(current_q_rev, prev_q_rev)

    return {"week": week_entry, "month": month_entry, "quarter": quarter_entry}
