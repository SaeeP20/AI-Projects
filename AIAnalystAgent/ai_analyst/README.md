# AI Business Analyst

Automatically analyses the Online Retail dataset and emails the CEO
a plain-English briefing every Monday morning.

## Setup

1. Install dependencies:
   pip install -r requirements.txt

2. Place your dataset in the data/ folder:
   data/Online Retail.xlsx

3. Set environment variables:
   export ANTHROPIC_API_KEY=your_key_here
   export EMAIL_SENDER=you@gmail.com
   export EMAIL_PASSWORD=your_app_password
   export CEO_EMAIL=ceo@example.com

4. Run immediately (for testing):
   python main.py --now

5. Run on a schedule (every Monday 07:00):
   python main.py

## Project structure

   ai_analyst/
   ├── data/
   │   ├── loader.py          # Load and clean the Excel file
   │   └── Online Retail.xlsx # Dataset goes here
   ├── analysis/
   │   ├── products.py        # Top products by revenue and quantity
   │   ├── trends.py          # Weekly sales, growth, country breakdown
   │   ├── churn.py           # RFM scoring and churn prediction
   │   └── anomalies.py       # Unusual week detection
   ├── report/
   │   ├── generate.py        # Sends metrics to Claude, gets CEO briefing
   │   └── email.py           # Emails the report
   ├── main.py                # Runs the full pipeline and scheduler
   └── requirements.txt
