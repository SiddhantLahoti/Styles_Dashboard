import os
import win32com.client  # pip install pywin32
import pandas as pd
from threading import Lock
from config import EXCEL_FILE_PATH, COL_DATE
import pythoncom

_df_cache = None
_last_modified_time = None
_lock = Lock()




import os
import win32com.client

def refresh_excel_file_via_app(filepath: str):
    """
    Opens Excel in the background, triggers 'Refresh All',
    waits for background queries to complete, saves, and closes.
    """
    abs_path = os.path.abspath(filepath)
    if not os.path.exists(abs_path):
        print(f"[WARNING] File not found: {abs_path}")
        return

    # 1. INITIALIZE COM FOR THIS THREAD
    pythoncom.CoInitialize()

    print("[INFO] Launching Excel in background to refresh queries...")
    excel = None
    wb = None
    try:
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False

        wb = excel.Workbooks.Open(Filename=abs_path, UpdateLinks=3, ReadOnly=False)
        if wb is None:
            print("[WARNING] Excel could not open the workbook.")
            return

        wb.RefreshAll()
        excel.CalculateUntilAsyncQueriesDone()
        wb.Save()
        print("[INFO] Excel data refreshed and saved successfully.")

    except Exception as e:
        print(f"[WARNING] Could not auto-refresh Excel file: {e}")
    finally:
        if wb:
            try:
                wb.Close(SaveChanges=False)
            except Exception:
                pass
        if excel:
            try:
                excel.Quit()
            except Exception:
                pass
        # 2. CLEAN UP COM FOR THIS THREAD
        pythoncom.CoUninitialize()
        
        
def load_data(force_reload: bool = False) -> pd.DataFrame:
    global _df_cache, _last_modified_time

    if not os.path.exists(EXCEL_FILE_PATH):
        raise FileNotFoundError(f"File not found: {EXCEL_FILE_PATH}")

    with _lock:
        # 1. PUT IT HERE: Refresh Excel on disk BEFORE reading into pandas
        if force_reload:
            try:
                refresh_excel_file_via_app(EXCEL_FILE_PATH)
            except Exception as e:
                print(f"[WARNING] Background Excel refresh skipped: {e}")

        # 2. Check the timestamp on the disk (it will now reflect the newly saved file)
        current_mtime = os.path.getmtime(EXCEL_FILE_PATH)

        # 3. Read into memory if not loaded, file modified, or force_reload is True
        if _df_cache is None or current_mtime != _last_modified_time or force_reload:
            print("[INFO] Loading / Refreshing Excel data into RAM...")
            df = pd.read_excel(EXCEL_FILE_PATH, sheet_name=0)
            
            # Clean string columns
            str_cols = ['drcd', 'DmCtg', 'DmSalCtg', 'Pdesc', 'Customer']
            for col in str_cols:
                if col in df.columns:
                    df[col] = df[col].fillna("-").astype(str)

            # Ensure date column is standard datetime
            if COL_DATE in df.columns:
                df[COL_DATE] = pd.to_datetime(df[COL_DATE], errors="coerce")

            _df_cache = df
            _last_modified_time = current_mtime
            print(f"[INFO] Loaded {len(df)} records successfully.")

    return _df_cache