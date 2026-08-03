import pandas as pd


def load_data(filepath: str) -> pd.DataFrame:
    """Load and clean the Online Retail dataset."""
    df = pd.read_excel(filepath, dtype={"CustomerID": str})

    # Drop rows with no customer (can't do churn analysis without them)
    df.dropna(subset=["CustomerID"], inplace=True)

    # Remove cancellations and returns (negative quantities)
    df = df[df["Quantity"] > 0]

    # Remove rows with no price
    df = df[df["UnitPrice"] > 0]

    # Add revenue column
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]

    # Parse dates (day-first format used in the dataset: DD/MM/YYYY)
    # Use errors='coerce' so invalid rows become NaT and can be inspected
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], dayfirst=True, errors="coerce")

    # If any InvoiceDate failed to parse, warn the user
    if df["InvoiceDate"].isna().any():
        n_bad = int(df["InvoiceDate"].isna().sum())
        print(f"Warning: {n_bad} rows have invalid InvoiceDate and will be dropped.")
        df = df.dropna(subset=["InvoiceDate"]) 

    return df
