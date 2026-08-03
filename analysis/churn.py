import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


def build_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build an RFM table — one row per customer with:
      Recency   — days since their last purchase
      Frequency — number of distinct invoices
      Monetary  — total revenue from that customer
    """
    snapshot = df["InvoiceDate"].max()

    rfm = df.groupby("CustomerID").agg(
        Recency=("InvoiceDate", lambda x: (snapshot - x.max()).days),
        Frequency=("InvoiceNo", "nunique"),
        Monetary=("Revenue", "sum"),
    ).reset_index()

    # Label: churned if no purchase in the last 90 days
    rfm["Churned"] = (rfm["Recency"] > 90).astype(int)

    return rfm


def predict_churn(rfm: pd.DataFrame) -> pd.DataFrame:
    """
    Train a Random Forest on the RFM features and attach a
    churn probability score to each customer.
    Returns the table sorted by highest risk first.
    """
    features = ["Recency", "Frequency", "Monetary"]
    X = rfm[features]
    y = rfm["Churned"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)

    rfm = rfm.copy()
    rfm["ChurnProbability"] = model.predict_proba(X_scaled)[:, 1].round(3)

    return rfm.sort_values("ChurnProbability", ascending=False)


def at_risk_customers(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """Return the top N customers most likely to churn."""
    rfm = build_rfm(df)
    scored = predict_churn(rfm)
    return scored.head(top_n)[["CustomerID", "Recency", "Frequency", "Monetary", "ChurnProbability"]]
