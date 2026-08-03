
import os
import pandas as pd
from datetime import datetime
from .dashboard import generate_dashboard_file
from .powerbi import export_results_to_excel, generate_powerbi_report


def build_metrics_summary(results: dict) -> str:
    """Turn the analysis results into a plain text summary to send to Claude."""
    growth = results["growth"]
    lines = [
        f"Report date: {datetime.today().strftime('%A %d %B %Y')}",
        "",
        "=== SALES GROWTH ===",
        f"This week's revenue: £{growth['current']:,.2f}",
        f"Last week's revenue: £{growth['previous']:,.2f}",
        f"Week-on-week change: {growth['growth_pct']:+.1f}%",
        "",
        "=== TOP 10 PRODUCTS BY REVENUE ===",
    ]

    for _, row in results["top_products"].iterrows():
        lines.append(f"  {row['Description']}: £{row['TotalRevenue']:,.2f}")

    lines += ["", "=== TOP 10 COUNTRIES BY REVENUE ==="]
    for _, row in results["countries"].head(10).iterrows():
        lines.append(f"  {row['Country']}: £{row['TotalRevenue']:,.2f}")

    lines += ["", "=== AT-RISK CUSTOMERS (top 10) ==="]
    for _, row in results["churn"].head(10).iterrows():
        lines.append(
            f"  Customer {row['CustomerID']} — "
            f"last purchase {int(row['Recency'])} days ago, "
            f"churn probability {row['ChurnProbability']:.0%}"
        )

    anomalies = results["anomalies"]
    lines += ["", "=== ANOMALIES DETECTED ==="]
    if anomalies.empty:
        lines.append("  No unusual weeks detected.")
    else:
        for _, row in anomalies.iterrows():
            lines.append(
                f"  {row['InvoiceDate'].strftime('%d %b %Y')}: "
                f"£{row['WeeklyRevenue']:,.0f} ({row['Direction']})"
            )

    return "\n".join(lines)


def generate_ceo_report(results: dict) -> dict:
    """
    Generate the report details for either Power BI or a local dashboard.

    Returns:
        dict with keys: 'summary', 'report_url', 'dashboard_file', 'export_file'
    """
    summary = build_metrics_summary(results)

    report_data = {
        "summary": summary,
        "report_url": None,
        "dashboard_file": None,
        "export_file": None,
    }

    use_powerbi = os.environ.get("USE_POWERBI", "false").lower() in {"1", "true", "yes"}
    if use_powerbi:
        report_url, export_file = generate_powerbi_report(results, None)
        report_data["report_url"] = report_url
        report_data["export_file"] = export_file

        if report_url is None:
            # Fallback if Power BI failed.
            dashboard_file = generate_dashboard_file(results)
            report_data["dashboard_file"] = dashboard_file
            if report_data["export_file"] is None:
                export_file = export_results_to_excel(results)
                report_data["export_file"] = export_file
    else:
        dashboard_file = generate_dashboard_file(results)
        export_file = export_results_to_excel(results)
        report_data["dashboard_file"] = dashboard_file
        report_data["export_file"] = export_file

    return report_data