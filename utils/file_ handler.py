# =========================
# TASK 1.1 — FILE HANDLER
# =========================
def read_sales_data(filename):
    encodings = ["utf-8", "latin-1", "cp1252"]
    raw_lines = []

    for enc in encodings:
        try:
            with open(filename, "r", encoding=enc, errors="replace") as f:
                lines = f.read().splitlines()
            break
        except FileNotFoundError:
            print(f"❌ File not found: {filename}")
            return []
        except Exception:
            continue
    else:
        print("❌ Failed to decode file.")
        return []

    lines = [line.strip() for line in lines if line.strip()]
    if lines and "TransactionID" in lines[0]:
        lines = lines[1:]

    return lines


# =========================
# TASK 1.2 — PARSE CLEAN
# =========================
def parse_transactions(raw_lines):
    transactions = []

    for line in raw_lines:
        parts = line.split("|")
        if len(parts) != 8:
            continue

        tid, date, pid, pname, qty, price, cid, region = parts

        pname = pname.replace(",", "")
        qty = qty.replace(",", "")
        price = price.replace(",", "")

        try:
            qty = int(qty)
            price = float(price)
        except ValueError:
            continue

        record = {
            "TransactionID": tid,
            "Date": date,
            "ProductID": pid,
            "ProductName": pname,
            "Quantity": qty,
            "UnitPrice": price,
            "CustomerID": cid,
            "Region": region
        }

        transactions.append(record)

    return transactions


# =========================
# TASK 1.3 — VALIDATION + FILTER
# =========================
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid = []
    invalid_count = 0

    for tx in transactions:
        tx["Amount"] = tx["Quantity"] * tx["UnitPrice"]

        if tx["Quantity"] <= 0 or tx["UnitPrice"] <= 0:
            invalid_count += 1
            continue
        if not tx["TransactionID"].startswith("T"):
            invalid_count += 1
            continue
        if not tx["ProductID"].startswith("P"):
            invalid_count += 1
            continue
        if not tx["CustomerID"].startswith("C"):
            invalid_count += 1
            continue

        valid.append(tx)

    summary = {
        "total_input": len(transactions),
        "invalid": invalid_count,
        "filtered_by_region": 0,
        "filtered_by_amount": 0,
        "final_count": 0
    }

    regions = sorted(set(tx["Region"] for tx in valid))
    amounts = [tx["Amount"] for tx in valid]
    print(f"Available Regions: {regions}")
    print(f"Amount Range: min={min(amounts):.2f}, max={max(amounts):.2f}")

    filtered = valid

    if region:
        before = len(filtered)
        filtered = [tx for tx in filtered if tx["Region"] == region]
        summary["filtered_by_region"] = before - len(filtered)
        print(f"After region filter ({region}): {len(filtered)} records")

    if min_amount is not None:
        before = len(filtered)
        filtered = [tx for tx in filtered if tx["Amount"] >= min_amount]
        summary["filtered_by_amount"] += before - len(filtered)

    if max_amount is not None:
        before = len(filtered)
        filtered = [tx for tx in filtered if tx["Amount"] <= max_amount]
        summary["filtered_by_amount"] += before - len(filtered)

    summary["final_count"] = len(filtered)

    return filtered, invalid_count, summary


# =========================
# MAIN EXECUTION PIPELINE
# =========================
if __name__ == "__main__":
    filename = "/Users/deepsaha/Documents/BITSOM learning/Module 3/data/sales_data.txt"   # <-- update if needed

    raw_lines = read_sales_data(filename)
    print(f"Loaded raw lines: {len(raw_lines)}")

    parsed = parse_transactions(raw_lines)
    print(f"Parsed transactions: {len(parsed)}")

    filtered, invalid_count, summary = validate_and_filter(
        parsed,
        region="North",        # optional
        min_amount=500,        # optional
        max_amount=50000       # optional
    )

    print("\nFinal Output Summary:")
    print(summary)
    print(f"Final valid records returned: {len(filtered)}")
