import math
import pandas as pd
from typing import Optional, List
from config import (
    COL_CODE, COL_CTG, COL_SAL_CTG, COL_PDESC, COL_DATE,
    COL_DIA_QTY, COL_DIA_CTS, COL_CUSTOMER, SEARCH_COLUMNS,COL_CS_QTY, COL_CS_CTS, COL_GLD_WT, COL_SIL_WT
)

def get_unique_filter_options(df: pd.DataFrame) -> dict:
    """Returns unique values for dropdowns and min/max ranges for sliders/inputs."""
    min_date = df[COL_DATE].min()
    max_date = df[COL_DATE].max()

    return {
        "categories": sorted([x for x in df[COL_CTG].dropna().unique() if x != "-"]),
        "sales_categories": sorted([x for x in df[COL_SAL_CTG].dropna().unique() if x != "-"]),
        "product_descriptions": sorted([x for x in df[COL_PDESC].dropna().unique() if x != "-"]),
        "customers": sorted([x for x in df[COL_CUSTOMER].dropna().unique() if x != "-"]),
        "ranges": {
            "min_date": str(min_date.date()) if pd.notnull(min_date) else None,
            "max_date": str(max_date.date()) if pd.notnull(max_date) else None,
            "min_dia_qty": int(df[COL_DIA_QTY].min()),
            "max_dia_qty": int(df[COL_DIA_QTY].max()),
            "min_dia_cts": float(df[COL_DIA_CTS].min()),
            "max_dia_cts": float(df[COL_DIA_CTS].max()),
            "min_cs_qty": int(df[COL_CS_QTY].min()),
            "max_cs_qty": int(df[COL_CS_QTY].max()),
            "min_cs_cts": float(df[COL_CS_CTS].min()),
            "max_cs_cts": float(df[COL_CS_CTS].max()),
            "min_gld_wt": float(df[COL_GLD_WT].min()),
            "max_gld_wt": float(df[COL_GLD_WT].max()),
            "min_sil_wt": float(df[COL_SIL_WT].min()),
            "max_sil_wt": float(df[COL_SIL_WT].max()),
        }
    }

def apply_filters_and_paginate(
    df: pd.DataFrame,
    search_query: Optional[str] = None,
    categories: Optional[List[str]] = None,          # <-- List instead of single str
    sales_categories: Optional[List[str]] = None,    # <-- List
    product_descs: Optional[List[str]] = None,       # <-- List
    customers: Optional[List[str]] = None,           # <-- List
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    min_qty: Optional[int] = None,
    max_qty: Optional[int] = None,
    min_cts: Optional[float] = None,
    max_cts: Optional[float] = None,
    min_cs_qty: Optional[int] = None,
    max_cs_qty: Optional[int] = None,
    min_cs_cts: Optional[float] = None,
    max_cs_cts: Optional[float] = None,
    min_gld_wt: Optional[float] = None,
    max_gld_wt: Optional[float] = None,
    min_sil_wt: Optional[float] = None,
    max_sil_wt: Optional[float] = None,
    page: int = 1,
    page_size: int = 24
) -> dict:
    """Filters data in memory and returns a paginated slice."""
    filtered_df = df

    # 1. Search Query across Columns A, B, C, D
    if search_query and search_query.strip():
        q = search_query.strip().lower()
        mask = (
            filtered_df[COL_CODE].str.lower().str.contains(q, na=False) |
            filtered_df[COL_CTG].str.lower().str.contains(q, na=False) |
            filtered_df[COL_SAL_CTG].str.lower().str.contains(q, na=False) |
            filtered_df[COL_PDESC].str.lower().str.contains(q, na=False)
        )
        filtered_df = filtered_df[mask]

    # 2. Multi-select Dropdown Filters (Cols B, C, D, L with OR condition)
    if categories:
        filtered_df = filtered_df[filtered_df[COL_CTG].isin(categories)]

    if sales_categories:
        filtered_df = filtered_df[filtered_df[COL_SAL_CTG].isin(sales_categories)]

    if product_descs:
        filtered_df = filtered_df[filtered_df[COL_PDESC].isin(product_descs)]

    if customers:
        filtered_df = filtered_df[filtered_df[COL_CUSTOMER].isin(customers)]
    # 3. Time Frame Filter (Column E)
    if start_date:
        filtered_df = filtered_df[filtered_df[COL_DATE] >= pd.to_datetime(start_date)]
    if end_date:
        filtered_df = filtered_df[filtered_df[COL_DATE] <= pd.to_datetime(end_date)]

    # 4. Quantity / Carats Range Filters (Columns F & G)
    if min_qty is not None:
        filtered_df = filtered_df[filtered_df[COL_DIA_QTY] >= min_qty]
    if max_qty is not None:
        filtered_df = filtered_df[filtered_df[COL_DIA_QTY] <= max_qty]

    if min_cts is not None:
        filtered_df = filtered_df[filtered_df[COL_DIA_CTS] >= min_cts]
    if max_cts is not None:
        filtered_df = filtered_df[filtered_df[COL_DIA_CTS] <= max_cts]
    
    # Col H: CSQty
    if min_cs_qty is not None:
        filtered_df = filtered_df[filtered_df[COL_CS_QTY] >= min_cs_qty]
    if max_cs_qty is not None:
        filtered_df = filtered_df[filtered_df[COL_CS_QTY] <= max_cs_qty]

    # Col I: Cscts
    if min_cs_cts is not None:
        filtered_df = filtered_df[filtered_df[COL_CS_CTS] >= min_cs_cts]
    if max_cs_cts is not None:
        filtered_df = filtered_df[filtered_df[COL_CS_CTS] <= max_cs_cts]

    # Col J: Gldwt
    if min_gld_wt is not None:
        filtered_df = filtered_df[filtered_df[COL_GLD_WT] >= min_gld_wt]
    if max_gld_wt is not None:
        filtered_df = filtered_df[filtered_df[COL_GLD_WT] <= max_gld_wt]

    # Col K: Silwt
    if min_sil_wt is not None:
        filtered_df = filtered_df[filtered_df[COL_SIL_WT] >= min_sil_wt]
    if max_sil_wt is not None:
        filtered_df = filtered_df[filtered_df[COL_SIL_WT] <= max_sil_wt]
    
    # --- Dynamic Sorting (Part 1 Updated) ---
    # 1. Check if ANY of the 6 numeric filters (DiaQty, DiaCts, CSQty, Cscts, Gldwt, Silwt) are active
    numeric_filter_applied = (
        min_qty is not None or max_qty is not None or
        min_cts is not None or max_cts is not None or
        min_cs_qty is not None or max_cs_qty is not None or
        min_cs_cts is not None or max_cs_cts is not None or
        min_gld_wt is not None or max_gld_wt is not None or
        min_sil_wt is not None or max_sil_wt is not None
    )

    if numeric_filter_applied:
        # Determine which metric was filtered, and sort by it in ascending order (lowest to highest)
        if min_gld_wt is not None or max_gld_wt is not None:
            sort_col = COL_GLD_WT
        elif min_sil_wt is not None or max_sil_wt is not None:
            sort_col = COL_SIL_WT
        elif min_cts is not None or max_cts is not None:
            sort_col = COL_DIA_CTS
        elif min_cs_cts is not None or max_cs_cts is not None:
            sort_col = COL_CS_CTS
        elif min_qty is not None or max_qty is not None:
            sort_col = COL_DIA_QTY
        else:
            sort_col = COL_CS_QTY

        filtered_df = filtered_df.sort_values(by=sort_col, ascending=True, na_position="last")
    else:
        # Default: Newest date first (descending)
        if COL_DATE in filtered_df.columns:
            filtered_df = filtered_df.sort_values(by=COL_DATE, ascending=False, na_position="last")
    # Total counts before pagination
    total_items = len(filtered_df)
    total_pages = math.ceil(total_items / page_size) if total_items > 0 else 1
    page = max(1, min(page, total_pages))

    # Slice for the current page
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    page_items = filtered_df.iloc[start_idx:end_idx].copy()

    # Convert timestamps to string format for JSON serialization
    if COL_DATE in page_items.columns:
        page_items[COL_DATE] = page_items[COL_DATE].dt.strftime("%d-%m-%Y").fillna("-")

    # Fill remaining NaNs for JSON safety
    page_items = page_items.fillna(0)

    return {
        "page": page,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": total_pages,
        "items": page_items.to_dict(orient="records")
    }