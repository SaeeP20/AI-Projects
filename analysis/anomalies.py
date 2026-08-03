import pandas as pd


def detect_anomalies(df: pd.DataFrame, window: int = 4, threshold: float = 2.0) -> pd.DataFrame:
    """
    Flag weeks where revenue is unusually high or low compared to
    a rolling average. Uses a simple z-score approach.

    window    — number of weeks to use for the rolling average
    threshold — how many standard deviations counts as unusual
    """
    weekly = (
        df.resample("W", on="InvoiceDate")["Revenue"]
        .sum()
        .reset_index()
        .rename(columns={"Revenue": "WeeklyRevenue"})
    )

    weekly["RollingMean"] = weekly["WeeklyRevenue"].rolling(window).mean()
    weekly["RollingStd"] = weekly["WeeklyRevenue"].rolling(window).std()

    weekly["ZScore"] = (
        (weekly["WeeklyRevenue"] - weekly["RollingMean"]) / weekly["RollingStd"]
    )

    weekly["Anomaly"] = weekly["ZScore"].abs() > threshold
    weekly["Direction"] = weekly["ZScore"].apply(
        lambda z: "spike" if z > threshold else ("drop" if z < -threshold else "normal")
    )

    return weekly[weekly["Anomaly"]][["InvoiceDate", "WeeklyRevenue", "ZScore", "Direction"]]
