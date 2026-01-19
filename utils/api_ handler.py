# utils/api_handler.py

import requests
import os

# ====================================
# Task 3.1 (a) — Fetch All Products
# ====================================
def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    
    Returns: list of product dictionaries in format:
    [
        {
            'id': 1,
            'title': 'iPhone 9',
            'category': 'smartphones',
            'brand': 'Apple',
            'price': 549,
            'rating': 4.69
        },
        ...
    ]
    """
    url = "https://dummyjson.com/products?limit=100"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        products = data.get("products", [])
        
        formatted = []
        for p in products:
            formatted.append({
                'id': p.get('id'),
                'title': p.get('title'),
                'category': p.get('category'),
                'brand': p.get('brand'),
                'price': p.get('price'),
                'rating': p.get('rating')
            })
        
        print(f"[SUCCESS] Fetched {len(formatted)} products from API")
        return formatted

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch products from API: {e}")
        return []


# ==============================================
# Task 3.1 (b) — Create Product Mapping (ID → Info)
# ==============================================
def create_product_mapping(api_products):
    """
    Creates mapping dictionary: { product_id: {...product info...} }
    
    Example output:
    {
        1: {'title': 'iPhone 9', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.69},
        2: {...}
    }
    """
    mapping = {}
    
    for p in api_products:
        mapping[p['id']] = {
            'title': p.get('title'),
            'category': p.get('category'),
            'brand': p.get('brand'),
            'rating': p.get('rating')
        }
    
    return mapping


# ====================================
# Task 3.2 — Enrich Sales Data
# ====================================
def enrich_sales_data(transactions, product_mapping):
    """
    Enriches each transaction with API details.
    
    New fields added:
    - API_Category
    - API_Brand
    - API_Rating
    - API_Match (True/False)
    
    Saving is done via `save_enriched_data()`
    """
    enriched = []
    
    for tx in transactions:
        new_tx = tx.copy()
        
        # Extract numeric part of ProductID (P101 → 101)
        try:
            numeric_id = int(new_tx["ProductID"].replace("P", "").strip())
        except:
            numeric_id = None
        
        if numeric_id in product_mapping:
            api_info = product_mapping[numeric_id]
            new_tx["API_Category"] = api_info.get('category')
            new_tx["API_Brand"] = api_info.get('brand')
            new_tx["API_Rating"] = api_info.get('rating')
            new_tx["API_Match"] = True
        else:
            new_tx["API_Category"] = None
            new_tx["API_Brand"] = None
            new_tx["API_Rating"] = None
            new_tx["API_Match"] = False
        
        enriched.append(new_tx)
    
    # Save to file after enriching
    save_enriched_data(enriched)
    
    return enriched


# ====================================
# Helper — Save Enriched Data
# ====================================
def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions to file using pipe delimiters.
    Creates folder if missing.
    """
    
    # Ensure output folder exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Header with new API fields
    header_fields = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("|".join(header_fields) + "\n")
        
        for tx in enriched_transactions:
            row = [
                str(tx.get("TransactionID", "")),
                str(tx.get("Date", "")),
                str(tx.get("ProductID", "")),
                str(tx.get("ProductName", "")),
                str(tx.get("Quantity", "")),
                str(tx.get("UnitPrice", "")),
                str(tx.get("CustomerID", "")),
                str(tx.get("Region", "")),
                str(tx.get("API_Category", "")),
                str(tx.get("API_Brand", "")),
                str(tx.get("API_Rating", "")),
                str(tx.get("API_Match", ""))
            ]
            f.write("|".join(row) + "\n")
    
    print(f"[SUCCESS] Enriched data saved to: {filename}")
