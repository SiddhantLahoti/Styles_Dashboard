import os

# Excel file path
EXCEL_FILE_PATH = os.path.join(os.path.dirname(__file__), "dsg det suvidha.xlsx")

# --- Image Folder Paths ---
# Replace with your actual paths (network shares or local drives)
PRIMARY_IMG_DIR = r"Y:\\"        # 1st Priority: Exact match
FALLBACK_IMG_DIR = r"Z:\LD"            # 2nd Priority: Recursive search

# Local cache directory for cropped thumbnails
IMAGE_CACHE_DIR = os.path.join(os.path.dirname(__file__), ".cache_images")

# Excel Column Definitions
COL_CODE = "drcd"         # Column A
COL_CTG = "DmCtg"         # Column B
COL_SAL_CTG = "DmSalCtg"  # Column C
COL_PDESC = "Pdesc"       # Column D
COL_DATE = "dmcrdt"       # Column E
COL_DIA_QTY = "DiaQty"    # Column F
COL_DIA_CTS = "DiaCts"    # Column G
COL_CS_QTY = "CSQty"      # Column H
COL_CS_CTS = "Cscts"      # Column I
COL_GLD_WT = "Gldwt"      # Column J
COL_SIL_WT = "Silwt"      # Column K
COL_CUSTOMER = "Customer" # Column L

SEARCH_COLUMNS = [COL_CODE, COL_CTG, COL_SAL_CTG, COL_PDESC]