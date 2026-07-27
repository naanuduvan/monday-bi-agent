from flask import Flask, request, jsonify
import pandas as pd
from monday_api import get_board_items
from business_logic import (
    total_pipeline_value,
    open_deals,
    won_deals,
    sector_summary,
    execution_summary,
    deals_this_quarter,
    deals_by_sector_this_quarter,
    sector_value_this_quarter,
    deals_by_quarter_with_fallback
)
from config import DEALS_BOARD_ID, WORK_BOARD_ID

app = Flask(__name__)

# Load data from Monday boards
def load_deals_data():
    items = get_board_items(DEALS_BOARD_ID)
    return pd.DataFrame(items)

def load_work_data():
    items = get_board_items(WORK_BOARD_ID)
    return pd.DataFrame(items)

# Map founder-style prompts to functions
PROMPT_MAP = {
    "total pipeline value": lambda df: total_pipeline_value(df),
    "open deals": lambda df: open_deals(df),
    "won deals": lambda df: won_deals(df),
    "sector summary": lambda df: sector_summary(df),
    "execution summary": lambda df: execution_summary(df),
    "deals this quarter": lambda df: deals_this_quarter(df),
    "mining pipeline this quarter": lambda df: deals_by_sector_this_quarter(df, "Mining"),
    "sector value this quarter": lambda df: sector_value_this_quarter(df),
    "deals by quarter": lambda df: deals_by_quarter_with_fallback(df),
}

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    prompt = data.get("prompt", "").lower()

    df = load_deals_data()

    if prompt in PROMPT_MAP:
        result = PROMPT_MAP[prompt](df)
        if isinstance(result, pd.Series):
            return jsonify(result.to_dict())
        elif isinstance(result, pd.DataFrame):
            return result.to_json(orient="records")
        else:
            return jsonify({"result": result})
    else:
        return jsonify({"error": "Unknown prompt"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
