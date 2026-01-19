# sales-analytics-system
Sales Analytics System

A complete end-to-end Python application that processes messy sales transaction files, enriches them with product data from an external API, performs sales analytics, and generates comprehensive business reports for decision-making.

📦 Features

✔ Reads and cleans messy sales transaction data
✔ Handles encoding issues and invalid records
✔ Supports filtering by region and transaction amount
✔ Analyzes sales revenue, customers, regions, and products
✔ Fetches real-time product data from DummyJSON API
✔ Enriches transactions with API product information
✔ Generates a well-formatted text-based analytics report
✔ Saves enriched output for further BI/analytics use
✔ Fully modular and production-friendly code structure

🗂️ Project Folder Structure
sales-analytics-system/
│
├── data/
│   ├── sales_data.txt              # Input sales data (provided dataset)
│   └── enriched_sales_data.txt     # Auto-generated enriched output
│
├── output/
│   └── sales_report.txt            # Auto-generated business report
│
├── utils/
│   ├── data_processor.py           # Sales analytics functions
│   ├── api_handler.py              # DummyJSON API integration + enrichment
│   └── report_generator.py         # Text report generator
│
├── filehandler.py                  # File reading, parsing, validation
├── main.py                         # Main application runner
├── requirements.txt                # Dependencies (requests, etc.)
├── README.md                       # Documentation
└── .gitignore                      # Cache & IDE ignore rules

🛠 Technologies Used

Python 3.8+

DummyJSON API

Standard Python libraries only:

os, datetime, collections

Third-party libraries:

requests

📥 Input Requirements

The input file:

Must be placed in: data/sales_data.txt

Pipe (|) delimited

May contain:

Encoding issues

Commas in product names or numeric fields

Invalid or missing values

📤 Generated Outputs

After running the application:

✔ Enriched Sales Data (for BI tools)
data/enriched_sales_data.txt


Contains:

Original transactional fields

API Category

API Brand

API Rating

API_Match flag

✔ Business Analytics Report
output/sales_report.txt


Includes:

Overall sales summary

Region performance

Top products/customers

Daily trends

API enrichment summary

Product performance insights

🚀 Setup & Installation
1. Clone Repository
git clone https://github.com/<your-username>/sales-analytics-system.git
cd sales-analytics-system

2. Install Dependencies

Make sure you have Python 3.8+ installed.

Then run:

pip install -r requirements.txt


Dependencies include:

requests

▶️ How to Run

Run the application from project root:

python3 main.py

🧪 User Interaction Flow

During execution, the system will:

Load sales data

Parse & clean transactions

Show available regions + amount ranges

Ask if you want to filter (y/n)

Validate transactions

Perform analytics

Fetch products from API

Enrich transactions

Save enriched data file

Generate analytics report

Sample console output:

[1/10] Reading sales data...
✓ Successfully read 95 records
...
[10/10] Process Complete!

🧾 Error Handling

This application gracefully handles:

File not found errors

Encoding errors

API request failures

Invalid transaction records

User input errors

No crash on runtime failures

📊 Supported Analytics

The system calculates:

Total revenue

Average order value

Region-wise performance

Top selling products

Top spending customers

Daily sales trends

Low-performing products

Peak sales day

API enrichment success rate

🌐 API Integration

Uses:

https://dummyjson.com/products


API used to enrich transactions with:

Category

Brand

Rating

API_Match flag

📌 Pre-Submission Checklist (Verified)

✔ Public repository
✔ Correct folder structure
✔ sales_data.txt placed in data/
✔ enriched_sales_data.txt generated
✔ sales_report.txt generated
✔ requirements.txt includes requests
✔ README.md contains setup + run instructions
✔ No hard-coded absolute paths
✔ Program runs end-to-end without crashing
✔ 10+ meaningful git commits

👨‍💻 Author

Name: Your Name Here