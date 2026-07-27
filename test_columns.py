from monday_api import run_query
from config import DEALS_BOARD_ID, WORK_BOARD_ID

def list_columns(board_id, board_name):
    query = f"""
    {{
      boards(ids: {board_id}) {{
        columns {{
          id
          title
          type
        }}
      }}
    }}
    """
    result = run_query(query)
    print(f"\n=== {board_name} Columns ===")
    for col in result["data"]["boards"][0]["columns"]:
        print(f"ID: {col['id']} | Title: {col['title']} | Type: {col['type']}")

if __name__ == "__main__":
    list_columns(DEALS_BOARD_ID, "Deals Board")
    list_columns(WORK_BOARD_ID, "Work Orders Board")
