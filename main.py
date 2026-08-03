import schedule
import time
import os

from data.loader import load_data
from analysis.products import top_products
from analysis.trends import (
    sales_by_week,
    sales_growth,
    sales_growth_multi,
    country_performance,
)
from analysis.churn import at_risk_customers
from analysis.anomalies import detect_anomalies
from report.generate import generate_ceo_report
from report.email import send_report

DATA_PATH = os.environ.get("DATA_PATH", "data/Online Retail.xlsx")
CEO_EMAIL = os.environ.get("CEO_EMAIL", "pujari.saee@gmail.com")
SCHEDULE_TIME = os.environ.get("SCHEDULE_TIME", "07:00")


def run_full_analysis(df):
    """Run all analysis modules and return results as a dict."""
    return {
        "top_products": top_products(df),
        "weekly_sales": sales_by_week(df),
        "growth":       sales_growth(df),
        "growth_multi": sales_growth_multi(df),
        "countries":    country_performance(df),
        "churn":        at_risk_customers(df),
        "anomalies":    detect_anomalies(df),
    }


def run_pipeline():
    """Load data, analyse, generate report, send email."""
    print("Loading data...")
    df = load_data(DATA_PATH)

    print("Running analysis...")
    results = run_full_analysis(df)

    print("Generating CEO report...")
    report = generate_ceo_report(results)

    print("\n--- REPORT PREVIEW ---")
    print(report.get("summary") if isinstance(report, dict) else report)
    print("----------------------\n")

    print("Sending email...")
    send_report(report, CEO_EMAIL)

    print("Done.")


if __name__ == "__main__":
    import sys

    if "--now" in sys.argv:
        # Run immediately: python main.py --now
        run_pipeline()
    else:
        # Schedule for every Monday at the configured time
        schedule.every().monday.at(SCHEDULE_TIME).do(run_pipeline)
        print(f"Scheduler running. Waiting for Mondays at {SCHEDULE_TIME}...")
        while True:
            schedule.run_pending()
            time.sleep(60)
