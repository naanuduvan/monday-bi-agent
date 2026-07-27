from flask import Flask, request, jsonify, send_from_directory
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
from config import DEALS_BOARD_ID

app = Flask(__name__)

# Serve index.html directly from root
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# Serve app.js directly from root
@app.route("/app.js")
def frontend_js():
    return send_from_directory(".", "app.js")

# API route for prompts
@app.route("/query", methods=["POST"])
def query():
    data = request.json
    prompt = data.get("prompt", "").lower()

    df = pd.DataFrame(get_board_items(DEALS_BOARD_ID))

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

    if prompt in PROMPT_MAP:
        result = PROMPT_MAP[prompt](df)

        # Fallback if empty or None
        if result is None or (hasattr(result, "empty") and result.empty):
            return jsonify({"message": "No data available for this query"})

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
