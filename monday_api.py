import requests
from config import MONDAY_API_KEY, DEALS_BOARD_ID, WORK_BOARD_ID

API_URL = "https://api.monday.com/v2"
headers = {
    "Authorization": MONDAY_API_KEY,
    "Content-Type": "application/json"
}

def run_query(query):
    """Send a GraphQL query to Monday.com and return the JSON response."""
    response = requests.post(API_URL, headers=headers, json={"query": query})
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code}\n{response.text}")
    data = response.json()
    if "errors" in data:
        raise Exception(data["errors"])
    return data

def fetch_board(board_id, column_ids=None):
    """
    Fetch items from a board.
    If column_ids is provided, only those columns will be returned.
    """
    if column_ids:
        ids_str = ", ".join([f'"{cid}"' for cid in column_ids])
        query = f"""
        {{
          boards(ids: {board_id}) {{
            id
            name
            items_page(limit: 100) {{
              items {{
                id
                name
                column_values(ids: [{ids_str}]) {{
                  id
                  text
                }}
              }}
            }}
          }}
        }}
        """
    else:
        # Default: fetch all columns
        query = f"""
        {{
          boards(ids: {board_id}) {{
            id
            name
            items_page(limit: 100) {{
              items {{
                id
                name
                column_values {{
                  id
                  text
                }}
              }}
            }}
          }}
        }}
        """

    data = run_query(query)
    return data["data"]["boards"][0]["items_page"]["items"]

def get_board_items(board_id):
    """
    Fetch all items from a board with all column values.
    Used by web_app.py for dashboards.
    """
    query = f"""
    {{
      boards(ids: {board_id}) {{
        items {{
          id
          name
          column_values {{
            id
            text
          }}
        }}
      }}
    }}
    """
    result = run_query(query)
    items = result["data"]["boards"][0]["items"]

    # Flatten into dicts for Pandas
    flattened = []
    for item in items:
        row = {"id": item["id"], "name": item["name"]}
        for col in item["column_values"]:
            row[col["id"]] = col["text"]
        flattened.append(row)

    return flattened

def get_deals():
    # Use the actual IDs from your Deals board
    return fetch_board(DEALS_BOARD_ID, column_ids=[
        "color_mm5n1c4g",      # Deal Status
        "numeric_mm5n112n",    # Masked Deal value
        "color_mm5nrjez"       # Sector/service
    ])

def get_work_orders():
    # Use the actual IDs from your Work Orders board
    return fetch_board(WORK_BOARD_ID, column_ids=[
        "color_mm5n56as",      # Execution Status
        "numeric_mm5nc8jf",    # Amount in Rupees (Excl of GST) (Masked)
        "numeric_mm5nd8vs"     # Amount in Rupees (Incl of GST) (Masked)
    ])

# Run this file directly to test the API
if __name__ == "__main__":
    print("Testing Monday.com API...\n")

    deals = get_deals()
    work_orders = get_work_orders()

    print(f"Deals Loaded: {len(deals)}")
    print(f"Work Orders Loaded: {len(work_orders)}")

    if len(deals) > 0:
        print("\nFirst Deal:")
        print(deals[0])

    if len(work_orders) > 0:
        print("\nFirst Work Order:")
        print(work_orders[0])
