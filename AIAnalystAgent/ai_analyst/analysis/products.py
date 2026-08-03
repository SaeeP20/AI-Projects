import pandas as pd


def top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return the top N products by total revenue."""
    return (
        df.groupby("Description")["Revenue"]
        .sum()
        .nlargest(n)
        .reset_index()
        .rename(columns={"Revenue": "TotalRevenue"})
    )


def top_products_by_quantity(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return the top N products by units sold."""
    return (
        df.groupby("Description")["Quantity"]
        .sum()
        .nlargest(n)
        .reset_index()
        .rename(columns={"Quantity": "UnitsSold"})
    )
