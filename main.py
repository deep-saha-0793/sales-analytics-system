
import sys
sys.path.append(".")


import pandas as pd
from datetime import datetime


from data import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import *

raw = read_sales_data("salesdata.txt")
parsed = parse_transactions(raw)
transactions, invalid_count, summary = validate_and_filter(parsed)

print("Total Revenue:", calculate_total_revenue(transactions))
print("Region Sales:", region_wise_sales(transactions))
print("Top Products:", top_selling_products(transactions))
print("Customer Analysis:", customer_analysis(transactions))
print("Daily Trend:", daily_sales_trend(transactions))
print("Peak Day:", find_peak_sales_day(transactions))
print("Low Performers:", low_performing_products(transactions))



FILE_PATH = "/Users/deepsaha/Documents/BITSOM learning/Module 3/data/sales_data.txt"

def clean_sales_file(filepath):
    # Read raw text lines
    with open(filepath, "r", errors="replace") as f:
        lines = f.read().splitlines()

    parsed_count = 0
    invalid_count = 0
    valid_records = []

    for line in lines:
        if not line.strip():
            continue

        parsed_count += 1

        parts = line.split("|")
        if len(parts) != 8:
            invalid_count += 1
            continue

        (
            transaction_id,
            date_str,
            product_id,
            product_name,
            quantity_str,
            unit_price_str,
            customer_id,
            region,
        ) = parts

        # Validation rules
        if not transaction_id.startswith("T"):
            invalid_count += 1
            continue

        if not customer_id or not region:
            invalid_count += 1
            continue

        # Clean commas inside fields
        product_name = product_name.replace(",", "")
        quantity_str = quantity_str.replace(",", "")
        unit_price_str = unit_price_str.replace(",", "")

        # Convert numeric fields
        try:
            quantity = int(quantity_str)
            unit_price = float(unit_price_str)
        except ValueError:
            invalid_count += 1
            continue

        if quantity <= 0 or unit_price <= 0:
            invalid_count += 1
            continue

        # Validate date
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            invalid_count += 1
            continue

        valid_records.append([
            transaction_id,
            date_obj,
            product_id,
            product_name,
            quantity,
            unit_price,
            customer_id,
            region,
            quantity * unit_price
        ])

    print(f"Total records parsed: {parsed_count}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(valid_records)}")

    df = pd.DataFrame(valid_records, columns=[
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region", "TotalAmount"
    ])
    return df


# ==== Execute Cleaning ====
df_cleaned = clean_sales_file(FILE_PATH)

print("\nPreview of cleaned data:")
print(df_cleaned.head())

print("\nSummary:")
print(df_cleaned.describe())

from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data

# Assume Part 1 already gives you validated transactions:
# transactions = [...]

api_products = fetch_all_products()
mapping = create_product_mapping(api_products)
enriched = enrich_sales_data(transactions, mapping)

print("Enrichment Complete!")

from utils.report_generator import generate_sales_report

generate_sales_report(transactions, enriched_transactions)


import sys
from filehandler import read_sales_data, parse_transactions, validate_and_filter
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data
from utils.report_generator import generate_sales_report


def main():
    try:
        print("=" * 40)
        print("       SALES ANALYTICS SYSTEM")
        print("=" * 40)
        print()

        # ---------------------------------------------------------
        # [1/10] Read Sales Data
        # ---------------------------------------------------------
        print("[1/10] Reading sales data...")

        raw = read_sales_data("salesdata.txt")
        print(f"✓ Successfully read {len(raw)} raw records\n")

        # ---------------------------------------------------------
        # [2/10] Parse and Clean
        # ---------------------------------------------------------
        print("[2/10] Parsing and cleaning data...")

        parsed = parse_transactions(raw)
        print(f"✓ Parsed {len(parsed)} records\n")

        # ---------------------------------------------------------
        # [3/10] Show Filter Options
        # ---------------------------------------------------------
        print("[3/10] Filter Options Available:")

        # derive region set
        regions = sorted(set(tx["Region"] for tx in parsed))
        print("Regions:", ", ".join(regions))

        # compute amount range
        amounts = [tx["Quantity"] * tx["UnitPrice"] for tx in parsed]
        min_amt, max_amt = min(amounts), max(amounts)
        print(f"Amount Range: ₹{min_amt:,.0f} - ₹{max_amt:,.0f}\n")

        # user filter choice
        apply_filter = input("Do you want to filter data? (y/n): ").strip().lower()
        region_filter, min_filter, max_filter = None, None, None

        if apply_filter == 'y':
            print("\nEnter filter values (press Enter to skip):")

            region_input = input(f"Region [{', '.join(regions)}]: ").strip()
            if region_input and region_input in regions:
                region_filter = region_input

            min_input = input("Minimum Amount: ").strip()
            if min_input.isdigit():
                min_filter = float(min_input)

            max_input = input("Maximum Amount: ").strip()
            if max_input.isdigit():
                max_filter = float(max_input)

        print()

        # ---------------------------------------------------------
        # [4/10] Validate + Apply Filters
        # ---------------------------------------------------------
        print("[4/10] Validating transactions...")

        valid_tx, invalid_count, summary = validate_and_filter(
            parsed,
            region=region_filter,
            min_amount=min_filter,
            max_amount=max_filter
        )

        print(f"✓ Valid: {len(valid_tx)} | Invalid: {invalid_count}")
        print()

        # ---------------------------------------------------------
        # [5/10] Perform Data Analysis
        # ---------------------------------------------------------
        print("[5/10] Analyzing sales data...")

        # Perform analyses to ensure no crashes later
        calculate_total_revenue(valid_tx)
        region_wise_sales(valid_tx)
        top_selling_products(valid_tx)
        customer_analysis(valid_tx)
        daily_sales_trend(valid_tx)
        find_peak_sales_day(valid_tx)
        low_performing_products(valid_tx)

        print("✓ Analysis complete\n")

        # ---------------------------------------------------------
        # [6/10] Fetch API Products
        # ---------------------------------------------------------
        print("[6/10] Fetching product data from API...")

        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products\n")

        # ---------------------------------------------------------
        # [7/10] Enrich Sales Data
        # ---------------------------------------------------------
        print("[7/10] Enriching sales data...")

        product_map = create_product_mapping(api_products)
        enriched = enrich_sales_data(valid_tx, product_map)

        enriched_count = sum(1 for tx in enriched if tx.get("API_Match"))
        success_rate = (enriched_count / len(enriched)) * 100 if enriched else 0

        print(f"✓ Enriched {enriched_count}/{len(enriched)} transactions ({success_rate:.1f}%)\n")

        # ---------------------------------------------------------
        # [8/10] Saving Enriched Data
        # ---------------------------------------------------------
        print("[8/10] Saving enriched data...")

        print("✓ Saved to: data/enriched_sales_data.txt\n")

        # ---------------------------------------------------------
        # [9/10] Generate Report
        # ---------------------------------------------------------
        print("[9/10] Generating report...")

        generate_sales_report(valid_tx, enriched)
        print("✓ Report saved to: output/sales_report.txt\n")

        # ---------------------------------------------------------
        # [10/10] Complete
        # ---------------------------------------------------------
        print("[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n[ERROR] An unexpected error occurred.")
        print("Details:", str(e))
        print("The application will now exit safely.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
