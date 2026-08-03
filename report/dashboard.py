from __future__ import annotations

import html
import os
from datetime import datetime
from pathlib import Path
from typing import Any


def _format_currency(value: float) -> str:
    return f"£{value:,.2f}"


def build_dashboard_html(results: dict[str, Any], report_date: str | None = None) -> str:
    """Build a simple standalone HTML dashboard without any Azure or external services."""
    growth = results["growth"]
    top_products = results["top_products"].head(10)
    countries = results["countries"].head(10)
    churn = results["churn"].head(10)
    anomalies = results["anomalies"]

    if report_date is None:
        report_date = datetime.today().strftime("%A %d %B %Y")

    def render_list(rows, label_key: str, value_key: str) -> str:
        if rows.empty:
            return '<p class="muted">No data available.</p>'

        items = []
        for _, row in rows.iterrows():
            label = html.escape(str(row[label_key]))
            value = _format_currency(float(row[value_key]))
            items.append(f"<li><span>{label}</span><strong>{value}</strong></li>")

        return f"<ul class='list'>{' '.join(items)}</ul>"

    top_products_html = render_list(top_products, "Description", "TotalRevenue")
    countries_html = render_list(countries, "Country", "TotalRevenue")

    churn_rows = []
    for _, row in churn.iterrows():
        churn_rows.append(
            f"<li><span>Customer {row['CustomerID']}</span><strong>{int(row['Recency'])} days • {row['ChurnProbability']:.0%}</strong></li>"
        )
    churn_html = f"<ul class='list'>{''.join(churn_rows)}</ul>" if churn_rows else '<p class="muted">No at-risk customers found.</p>'

    anomaly_rows = []
    for _, row in anomalies.iterrows():
        anomaly_rows.append(
            f"<li><span>{row['InvoiceDate'].strftime('%d %b %Y')}</span><strong>{_format_currency(float(row['WeeklyRevenue']))} • {row['Direction']}</strong></li>"
        )
    anomalies_html = f"<ul class='list'>{''.join(anomaly_rows)}</ul>" if anomaly_rows else '<p class="muted">No anomalies detected.</p>'

    html_content = f"""
    <!DOCTYPE html>
    <html lang='en'>
    <head>
      <meta charset='utf-8' />
      <title>Weekly Business Dashboard</title>
      <style>
        body {{
          font-family: Segoe UI, Arial, sans-serif;
          margin: 0;
          background: #f4f7fb;
          color: #16324f;
        }}
        .page {{ padding: 24px; }}
        h1 {{ margin-bottom: 8px; }}
        .subtitle {{ color: #5b6b7a; margin-bottom: 20px; }}
        .grid {{ display: grid; gap: 16px; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }}
        .card {{
          background: white;
          border-radius: 14px;
          padding: 16px 18px;
          box-shadow: 0 8px 18px rgba(0,0,0,0.06);
        }}
        .metric {{ font-size: 24px; font-weight: 700; margin-top: 6px; }}
        .label {{ color: #6b7a8f; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em; }}
        .list {{ list-style: none; padding: 0; margin: 10px 0 0; }}
        .list li {{ display: flex; justify-content: space-between; gap: 10px; padding: 8px 0; border-bottom: 1px solid #eef2f6; }}
        .list li:last-child {{ border-bottom: none; }}
        .muted {{ color: #728291; font-style: italic; }}
      </style>
    </head>
    <body>
      <div class='page'>
        <h1>Weekly Business Dashboard</h1>
        <div class='subtitle'>Generated on {report_date}</div>

        <div class='grid'>
          <div class='card'>
            <div class='label'>This week</div>
            <div class='metric'>{_format_currency(float(growth['current']))}</div>
          </div>
          <div class='card'>
            <div class='label'>Last week</div>
            <div class='metric'>{_format_currency(float(growth['previous']))}</div>
          </div>
          <div class='card'>
            <div class='label'>Week-on-week change</div>
            <div class='metric'>{growth['growth_pct']:+.1f}%</div>
          </div>
          <div class='card'>
            <div class='label'>Anomalies</div>
            <div class='metric'>{len(anomalies)}</div>
          </div>
        </div>

        <div class='grid' style='margin-top: 16px;'>
          <div class='card'>
            <h3>Top products</h3>
            {top_products_html}
          </div>
          <div class='card'>
            <h3>Top countries</h3>
            {countries_html}
          </div>
        </div>

        <div class='grid' style='margin-top: 16px;'>
          <div class='card'>
            <h3>At-risk customers</h3>
            {churn_html}
          </div>
          <div class='card'>
            <h3>Anomalies detected</h3>
            {anomalies_html}
          </div>
        </div>
      </div>
    </body>
    </html>
    """
    return html_content


def generate_dashboard_file(results: dict[str, Any], output_dir: str | None = None, filename: str | None = None) -> str:
    """Create an HTML dashboard file and return its path."""
    if output_dir is None:
        output_dir = os.path.join(os.getcwd(), "reports")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if filename is None:
        filename = f"weekly_dashboard_{datetime.today().strftime('%Y%m%d_%H%M%S')}.html"

    target_path = output_path / filename
    target_path.write_text(build_dashboard_html(results), encoding="utf-8")
    return str(target_path)
