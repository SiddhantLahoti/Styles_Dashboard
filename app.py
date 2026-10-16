from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import Response, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional, List
from contextlib import asynccontextmanager
from pydantic import BaseModel
from data_loader import load_data
from filters import get_unique_filter_options, apply_filters_and_paginate
from image_service import index_image_directories, find_image_for_style, get_cropped_image_bytes, generate_shortlist_excel , generate_catalogue_excel
import threading
from contextlib import asynccontextmanager

sync_status = {
    "is_ready": False,
    "step": "Initializing engine...",
    "records": 0,
    "images": 0
}

def background_initial_sync():
    """Runs heavy Excel loading and image indexing in background after port opens."""
    global sync_status
    try:
        sync_status["step"] = "Refreshing and loading Excel records..."
        df = load_data(force_reload=True)
        sync_status["records"] = len(df)

        sync_status["step"] = "Indexing jewelry image directories..."
        index_image_directories()
        from image_service import _primary_index, _fallback_files
        sync_status["images"] = len(_primary_index) + len(_fallback_files)

        sync_status["step"] = "Ready"
        sync_status["is_ready"] = True
        print("[INFO] Background initial sync complete! Application ready.")
    except Exception as e:
        sync_status["step"] = f"Error: {e}"
        print(f"[ERROR] Initial sync failed: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the server port immediately, run heavy work in background thread
    t = threading.Thread(target=background_initial_sync, daemon=True)
    t.start()
    yield

app = FastAPI(title="Design Catalog Dashboard", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_home():
    return FileResponse("static/index.html")

@app.get("/api/status")
def api_get_status():
    """Polled by frontend until dataset is loaded."""
    return sync_status

# 1. Update the image endpoint to support the 'full' parameter
@app.get("/api/image/{style_code}")
def api_get_product_image(style_code: str, full: bool = False):
    matched_path = find_image_for_style(style_code)
    if not matched_path:
        raise HTTPException(status_code=404, detail="Image not found")

    try:
        img_bytes = get_cropped_image_bytes(matched_path, full_resolution=full)
        return Response(content=img_bytes, media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/filters")
def api_get_filters():
    df = load_data()
    return get_unique_filter_options(df)

@app.get("/api/products")
def api_get_products(
    search: Optional[str] = None,
    category: Optional[List[str]] = Query(None),          # <-- Accept list
    sales_category: Optional[List[str]] = Query(None),    # <-- Accept list
    product_desc: Optional[List[str]] = Query(None),      # <-- Accept list
    customer: Optional[List[str]] = Query(None),          # <-- Accept list 
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
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=24, ge=12, le=96)
):
    df = load_data()
    return apply_filters_and_paginate(
        df=df,
        search_query=search,
        categories=category,
        sales_categories=sales_category,
        product_descs=product_desc,
        customers=customer,
        start_date=start_date,
        end_date=end_date,
        min_qty=min_qty,
        max_qty=max_qty,
        min_cts=min_cts,
        max_cts=max_cts,
        min_cs_qty=min_cs_qty,
        max_cs_qty=max_cs_qty,
        min_cs_cts=min_cs_cts,
        max_cs_cts=max_cs_cts,
        min_gld_wt=min_gld_wt,
        max_gld_wt=max_gld_wt,
        min_sil_wt=min_sil_wt,
        max_sil_wt=max_sil_wt,
        page=page,
        page_size=page_size
    )
    
# 2. Endpoint to fetch all items matching the active filters (for "Shortlist All")
@app.get("/api/products/all-filtered")
def api_get_all_filtered_products(
    search: Optional[str] = None,
    category: Optional[List[str]] = Query(None),
    sales_category: Optional[List[str]] = Query(None),
    product_desc: Optional[List[str]] = Query(None),
    customer: Optional[List[str]] = Query(None),
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
    max_sil_wt: Optional[float] = None
):
    df = load_data()
    # Call filter function with huge page_size to return all matching records
    res = apply_filters_and_paginate(
        df=df,
        search_query=search,
        categories=category,
        sales_categories=sales_category,
        product_descs=product_desc,
        customers=customer,
        start_date=start_date,
        end_date=end_date,
        min_qty=min_qty,
        max_qty=max_qty,
        min_cts=min_cts,
        max_cts=max_cts,
        min_cs_qty=min_cs_qty,
        max_cs_qty=max_cs_qty,
        min_cs_cts=min_cs_cts,
        max_cs_cts=max_cs_cts,
        min_gld_wt=min_gld_wt,
        max_gld_wt=max_gld_wt,
        min_sil_wt=min_sil_wt,
        max_sil_wt=max_sil_wt,
        page=1,
        page_size=200000  # Return all matching rows
    )
    return {"items": res["items"]}

# 3. Export Shortlist with Images Endpoint
class ExportPayload(BaseModel):
    items: List[dict]
    per_row: Optional[int] = 5

@app.post("/api/export-shortlist")
def api_export_shortlist(payload: ExportPayload):
    if not payload.items:
        raise HTTPException(status_code=400, detail="No items to export")
    
    excel_stream = generate_shortlist_excel(payload.items)
    headers = {
        'Content-Disposition': 'attachment; filename="shortlisted_products.xlsx"'
    }
    return Response(
        content=excel_stream.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )

@app.post("/api/refresh")
def api_force_refresh():
    """Manual trigger endpoint to reload file immediately"""
    df = load_data(force_reload=True)
    return {"status": "success", "total_records": len(df)}

@app.post("/api/export-catalogue")
def api_export_catalogue(payload: ExportPayload):
    if not payload.items:
        raise HTTPException(status_code=400, detail="No items to export")

    per_row = payload.per_row if payload.per_row in [3, 4, 5] else 4
    excel_stream = generate_catalogue_excel(payload.items, per_row=per_row)
    headers = {
        'Content-Disposition': f'attachment; filename="Catalogue_{per_row}_per_row.xlsx"'
    }
    return Response(
        content=excel_stream.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)