import pandas as pd
import json
from datetime import datetime, timedelta

def safe_date(val):
    try:
        # If it's already a datetime object, return as is
        if isinstance(val, (datetime, pd.Timestamp)):
            return val.strftime("%Y-%m-%d")

        # If it's a string, try different formats
        if isinstance(val, str):
            # Try parsing with different formats
            formats = [
                "%m/%d/%Y",  # MM/DD/YYYY
                "%d/%m/%Y",  # DD/MM/YYYY
                "%Y-%m-%d",  # YYYY-MM-DD
                "%d-%m-%Y"   # DD-MM-YYYY
            ]
            
            for fmt in formats:
                try:
                    dt = pd.to_datetime(val, format=fmt)
                    return dt.strftime("%Y-%m-%d")
                except:
                    continue

            # If all format parsing fails, try splitting the string
            try:
                # Try different separators
                for sep in ['/', '-']:
                    if sep in val:
                        parts = val.split(sep)
                        if len(parts) == 3:
                            # Try different orderings
                            try:
                                # Try MM/DD/YYYY
                                month, day, year = map(int, parts)
                                dt = datetime(year, month, day)
                                return dt.strftime("%Y-%m-%d")
                            except:
                                try:
                                    # Try DD/MM/YYYY
                                    day, month, year = map(int, parts)
                                    dt = datetime(year, month, day)
                                    return dt.strftime("%Y-%m-%d")
                                except:
                                    continue
            except:
                pass

        return None

    except Exception as e:
        print(f"Error converting date: {str(e)}")
        return None

def safe_float(val):
    try:
        return float(val)
    except:
        return None

def clean_nans(obj):
    if isinstance(obj, float) and pd.isna(obj):
        return None
    elif isinstance(obj, (datetime, pd.Timestamp)):
        return obj.strftime("%Y-%m-%d")
    elif isinstance(obj, dict):
        return {k: clean_nans(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nans(v) for v in obj]
    else:
        return obj

def process_sheet(df, sheet_name):
    sales = []
    payments = []
    for _, row in df.iterrows():
        # Skip header rows like 'ITEM'
        if str(row[1]).strip().upper() in ["ITEM", "ITEMS"]:
            continue

        # If it has a product (sale)
        if pd.notna(row[1]):
            sales.append({
                "date": safe_date(row[0]),
                "item": str(row[1]).strip(),
                "quantity": safe_float(row[2]),
                "unit_price": safe_float(row[3]),
                "total_amount": safe_float(row[4]),
                "remain": safe_float(row[7]) if len(row) > 7 else None,
                "remark": str(row[8]).strip() if len(row) > 8 and pd.notna(row[8]) else None
            })

        # If it's a payment row
        elif pd.isna(row[1]) and (pd.notna(row[5]) or pd.notna(row[6]) or pd.notna(row[7])):
            payments.append({
                "deposited_date": safe_date(row[5]),
                "bank": safe_float(row[7]),
                "remark": str(row[6]).strip() if pd.notna(row[6]) else None
            })

    return {
        "client_name": sheet_name.strip(),
        "sales": sales,
        "payments": payments
    }

# === Run it ===

file_path = "EMRA - Tot Sales.xlsx"
excel_file = pd.ExcelFile(file_path)

all_clients = []
for sheet_name in excel_file.sheet_names:
    df = excel_file.parse(sheet_name, header=None)
    client_data = process_sheet(df, sheet_name)
    all_clients.append(client_data)

# Clean NaNs
all_clients = clean_nans(all_clients)

# Save to file
output_path = "emra_sales_output.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_clients, f, indent=2, ensure_ascii=False)

print(f"✅ JSON saved to {output_path}")
print(f"📄 {len(all_clients)} clients processed.") 