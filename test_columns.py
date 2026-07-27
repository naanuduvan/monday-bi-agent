from monday_api import run_query
from config import DEALS_BOARD_ID, WORK_BOARD_ID

# Query to list all columns for Deals board
deals_query = f"""
{{
  boards(ids: {DEALS_BOARD_ID}) {{
    columns {{
      id
      title
    }}
  }}
}}
"""

# Query to list all columns for Work Orders board
work_query = f"""
{{
  boards(ids: {WORK_BOARD_ID}) {{
    columns {{
      id
      title
    }}
  }}
}}
"""

print("=== Deals Board Columns ===")
print(run_query(deals_query))

print("\n=== Work Orders Board Columns ===")
print(run_query(work_query))
