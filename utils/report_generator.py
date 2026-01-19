# utils/report_generator.py

import os
from datetime import datetime
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)


def format_currency(amount):
    return f"₹{amount:,.2f}"


def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    report_lines = []

    # --------------------------------------------------
    # 1. HEADER
    # --------------------------------------------------
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_records = len(transactions)

    report_lines.append("=" * 60)
    report_lines.append(f"{'SALES ANALYTICS REPORT':^60}")
    report_lines.append(f"Generated: {now:^60}")
    report_lines.append(f"Records Processed: {total_records:^60}")
    report_lines.append("=" * 60)
    report_lines.append("\n")

    # --------------------------------------------------
    # 2. OVERALL SUMMARY
    # --------------------------------------------------
    revenue = calculate_total_revenue(transactions)
    avg_order_value = revenue / total_records if total_records > 0 else 0

    # date range
    dates = sorted(set([tx["Date"] for tx in transactions]))
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

    report_lines.append("OVERALL SUMMARY")
    report_lines.append("-" * 60)
    report_lines.append(f"Total Revenue:\t\t{format_currency(revenue)}")
    report_lines.append(f"Total Transactions:\t{total_records}")
    report_lines.append(f"Average Order Value:\t{format_currency(avg_order_value)}")
    report_lines.append(f"Date Range:\t\t{date_range}")
    report_lines.append("\n")

    # --------------------------------------------------
    # 3. REGION-WISE PERFORMANCE
    # --------------------------------------------------
    region_stats = region_wise_sales(transactions)

    report_lines.append("REGION-WISE PERFORMANCE")
    report_lines.append("-" * 60)
    report_lines.append(f"{'Region':<10}{'Sales':<20}{'% of Total':<15}{'Transactions'}")
    total_sales = revenue

    for region, stats in region_stats.items():
        report_lines.append(
            f"{region:<10}{format_currency(stats['total_sales']):<20}"
            f"{stats['percentage']:.2f}%{'':<5}{stats['transaction_count']}"
        )
    report_lines.append("\n")

    # --------------------------------------------------
    # 4. TOP 5 PRODUCTS
    # --------------------------------------------------
    report_lines.append("TOP 5 PRODUCTS")
    report_lines.append("-" * 60)
    report_lines.append(f"{'Rank':<6}{'Product':<20}{'Qty Sold':<12}{'Revenue'}")

    top_products = top_selling_products(transactions, n=5)
    for i, (pname, qty, rev) in enumerate(top_products, start=1):
        report_lines.append(
            f"{i:<6}{pname:<20}{qty:<12}{format_currency(rev)}"
        )
    report_lines.append("\n")

    # --------------------------------------------------
    # 5. TOP 5 CUSTOMERS
    # --------------------------------------------------
    customers = customer_analysis(transactions)
    report_lines.append("TOP 5 CUSTOMERS")
    report_lines.append("-" * 60)
    report_lines.append(f"{'Rank':<6}{'Customer':<12}{'Total Spent':<18}{'Orders'}")

    for i, (cid, stats) in enumerate(customers.items(), start=1):
        if i > 5: break
        report_lines.append(
            f"{i:<6}{cid:<12}{format_currency(stats['total_spent']):<18}{stats['purchase_count']}"
        )
    report_lines.append("\n")

    # --------------------------------------------------
    # 6. DAILY SALES TREND
    # --------------------------------------------------
    daily_stats = daily_sales_trend(transactions)

    report_lines.append("DAILY SALES TREND")
    report_lines.append("-" * 60)
    report_lines.append(f"{'Date':<14}{'Revenue':<18}{'Transactions':<15}{'Unique Cust.'}")

    for date, stats in daily_stats.items():
        report_lines.append(
            f"{date:<14}{format_currency(stats['revenue']):<18}"
            f"{stats['transaction_count']:<15}{stats['unique_customers']}"
        )
    report_lines.append("\n")

    # --------------------------------------------------
    # 7. PRODUCT PERFORMANCE ANALYSIS
    # --------------------------------------------------
    peak_day, peak_rev, peak_txn = find_peak_sales_day(transactions)
    low_perf = low_performing_products(transactions, threshold=10)

    # Avg transaction per region
    region_avg_val = {r: (region_stats[r]['total_sales'] / region_stats[r]['transaction_count'])
                      for r in region_stats}

    report_lines.append("PRODUCT PERFORMANCE ANALYSIS")
    report_lines.append("-" * 60)
    report_lines.append(f"Best Selling Day: {peak_day} (Revenue: {format_currency(peak_rev)}, Transactions: {peak_txn})")

    if low_perf:
        report_lines.append("\nLow Performing Products (Qty < 10):")
        report_lines.append(f"{'Product':<20}{'Qty':<10}{'Revenue'}")
        for pname, qty, rev in low_perf:
            report_lines.append(f"{pname:<20}{qty:<10}{format_currency(rev)}")
    else:
        report_lines.append("\nLow Performing Products: None")

    report_lines.append("\n\nAverage Transaction Value Per Region:")
    for r, val in region_avg_val.items():
        report_lines.append(f"  {r}: {format_currency(val)}")
    report_lines.append("\n")

    # --------------------------------------------------
    # 8. API ENRICHMENT SUMMARY
    # --------------------------------------------------
    report_lines.append("API ENRICHMENT SUMMARY")
    report_lines.append("-" * 60)

    total = len(enriched_transactions)
    success = sum(1 for tx in enriched_transactions if tx.get("API_Match"))
    fail = total - success
    success_rate = (success / total * 100) if total > 0 else 0

    failed_products = [
        tx["ProductID"] for tx in enriched_transactions if not tx.get("API_Match")
    ]

    report_lines.append(f"Total Enriched Records:\t{total}")
    report_lines.append(f"Successful Matches:\t{success}")
    report_lines.append(f"Failed Matches:\t\t{fail}")
    report_lines.append(f"Success Rate:\t\t{success_rate:.2f}%")

    if failed_products:
        report_lines.append("\nProducts Not Enriched:")
        for pid in failed_products:
            report_lines.append(f"  - {pid}")
    else:
        report_lines.append("\nAll Products Successfully Enriched")

    # --------------------------------------------------
    # WRITE OUTPUT FILE
    # --------------------------------------------------
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"[SUCCESS] Sales report generated at: {output_file}")
