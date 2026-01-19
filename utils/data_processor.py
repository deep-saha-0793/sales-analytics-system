# utils/data_processor.py

from collections import defaultdict
from datetime import datetime


# =====================================
# Task 2.1 (a) — Total Revenue
# =====================================
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions.
    Returns: float
    """
    total = 0.0
    for tx in transactions:
        total += tx["Quantity"] * tx["UnitPrice"]
    return float(total)


# =====================================
# Task 2.1 (b) — Region-wise Sales
# =====================================
def region_wise_sales(transactions):
    """
    Returns region-wise sales statistics sorted by total sales desc.
    Format:
    {
        'North': {'total_sales': ..., 'transaction_count': ..., 'percentage': ...},
        ...
    }
    """
    region_stats = defaultdict(lambda: {"total_sales": 0.0, "transaction_count": 0})
    
    # Calculate totals & counts
    for tx in transactions:
        amount = tx["Quantity"] * tx["UnitPrice"]
        region = tx["Region"]
        region_stats[region]["total_sales"] += amount
        region_stats[region]["transaction_count"] += 1
    
    # Calculate global total for percentage
    global_total = sum(r["total_sales"] for r in region_stats.values())
    
    # Add percentage and sort
    final = {}
    for region, stats in region_stats.items():
        stats["percentage"] = (stats["total_sales"] / global_total * 100) if global_total else 0
        final[region] = stats
    
    # Sort by total_sales desc
    final = dict(sorted(final.items(), key=lambda x: x[1]["total_sales"], reverse=True))
    
    return final


# =====================================
# Task 2.1 (c) — Top Selling Products
# =====================================
def top_selling_products(transactions, n=5):
    """
    Returns top n products sorted by total quantity sold.
    Format list of tuples:
    [
        (ProductName, TotalQuantity, TotalRevenue),
        ...
    ]
    """
    product_map = defaultdict(lambda: {"qty": 0, "rev": 0.0})
    
    for tx in transactions:
        pname = tx["ProductName"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        product_map[pname]["qty"] += tx["Quantity"]
        product_map[pname]["rev"] += amount
    
    # convert to tuples
    result = [
        (pname, vals["qty"], vals["rev"])
        for pname, vals in product_map.items()
    ]
    
    # sort by qty desc
    result.sort(key=lambda x: x[1], reverse=True)
    
    return result[:n]


# =====================================
# Task 2.1 (d) — Customer Purchase Analysis
# =====================================
def customer_analysis(transactions):
    """
    Returns customer purchase metrics sorted by total_spent desc.
    Format:
    {
        'C001': {
            'total_spent': ...,
            'purchase_count': ...,
            'avg_order_value': ...,
            'products_bought': [...]
        },
        ...
    }
    """
    cust_map = defaultdict(lambda: {
        "total_spent": 0.0,
        "purchase_count": 0,
        "products": set()
    })
    
    for tx in transactions:
        cid = tx["CustomerID"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        cust_map[cid]["total_spent"] += amount
        cust_map[cid]["purchase_count"] += 1
        cust_map[cid]["products"].add(tx["ProductName"])
    
    # build final output
    final = {}
    for cid, stats in cust_map.items():
        total = stats["total_spent"]
        count = stats["purchase_count"]
        final[cid] = {
            "total_spent": total,
            "purchase_count": count,
            "avg_order_value": (total / count) if count else 0,
            "products_bought": list(stats["products"])
        }
    
    # sort by total_spent descending
    final = dict(sorted(final.items(), key=lambda x: x[1]["total_spent"], reverse=True))
    
    return final


# =====================================
# Task 2.2 (a) — Daily Sales Trend
# =====================================
def daily_sales_trend(transactions):
    """
    Returns chronological daily sales trends.
    Format:
    {
        'YYYY-MM-DD': {
            'revenue': ...,
            'transaction_count': ...,
            'unique_customers': ...
        },
        ...
    }
    """
    day_map = defaultdict(lambda: {"revenue": 0.0, "transaction_count": 0, "customers": set()})
    
    for tx in transactions:
        date_str = tx["Date"]  # expected format 'YYYY-MM-DD'
        amount = tx["Quantity"] * tx["UnitPrice"]
        day_map[date_str]["revenue"] += amount
        day_map[date_str]["transaction_count"] += 1
        day_map[date_str]["customers"].add(tx["CustomerID"])
    
    # build final sorted chronologically
    final = {}
    for date_str, stats in sorted(day_map.items(), key=lambda x: datetime.strptime(x[0], "%Y-%m-%d")):
        final[date_str] = {
            "revenue": stats["revenue"],
            "transaction_count": stats["transaction_count"],
            "unique_customers": len(stats["customers"])
        }
    
    return final


# =====================================
# Task 2.2 (b) — Peak Sales Day
# =====================================
def find_peak_sales_day(transactions):
    """
    Returns (date, revenue, transaction_count)
    """
    daily = daily_sales_trend(transactions)
    
    peak_day = max(daily.items(), key=lambda x: x[1]["revenue"])
    
    date = peak_day[0]
    revenue = peak_day[1]["revenue"]
    count = peak_day[1]["transaction_count"]
    
    return (date, revenue, count)


# =====================================
# Task 2.3 (a) — Low Performing Products
# =====================================
def low_performing_products(transactions, threshold=10):
    """
    Returns list of (ProductName, TotalQuantity, TotalRevenue)
    for products with quantity < threshold sorted qty asc.
    """
    product_map = defaultdict(lambda: {"qty": 0, "rev": 0.0})
    
    for tx in transactions:
        pname = tx["ProductName"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        product_map[pname]["qty"] += tx["Quantity"]
        product_map[pname]["rev"] += amount
    
    # filter low performers
    low = [
        (pname, vals["qty"], vals["rev"])
        for pname, vals in product_map.items()
        if vals["qty"] < threshold
    ]
    
    # sort by qty ascending
    low.sort(key=lambda x: x[1])
    
    return low
