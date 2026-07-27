from flask import Flask, request, render_template_string
import plotly.express as px
from plotly.io import to_html

from monday_api import get_deals, get_work_orders
from data_processor import board_to_dataframe, convert_numeric
from prompts import interpret_query
from business_logic import (
    sector_summary,
    deals_by_quarter_with_fallback,
    sector_value_this_quarter,
    deals_this_quarter   # <-- NEW import
)

app = Flask(__name__)

# Load data once at startup
deals = get_deals()
work_orders = get_work_orders()
deals_df = convert_numeric(board_to_dataframe(deals), ["numeric_mm5n112n"])
work_df = convert_numeric(board_to_dataframe(work_orders), ["numeric_mm5nc8jf", "numeric_mm5nd8vs"])

HTML_TEMPLATE = """
<!doctype html>
<title>Founder BI Agent</title>
<h1>Founder BI Agent</h1>

<form method="post">
  <label>Ask a question:</label><br>
  <input type="text" name="query" style="width:400px">
  <input type="submit" value="Ask">
</form>

<h2>Quick Dashboards</h2>
<form method="post">
  <button name="preset" value="overview">Overview</button>
  <button name="preset" value="sector">Sector Breakdown</button>
  <button name="preset" value="quarterly">Quarterly Trend</button>
</form>

{% if answer %}
  <h2>Answer:</h2>
  <pre>{{ answer }}</pre>
{% endif %}
{% if chart %}
  <h2>Chart:</h2>
  {{ chart|safe }}
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def home():
    answer = None
    chart_html = None

    if request.method == "POST":
        # Handle preset dashboards
        if "preset" in request.form:
            preset = request.form["preset"]

            if preset == "overview":
                answer = f"Total Pipeline Value: {deals_df['numeric_mm5n112n'].sum()}"
            elif preset == "sector":
                result = sector_summary(deals_df)
                answer = str(result)
                fig = px.bar(result, x=result.index, y=result.values, title="Deals by Sector")
                chart_html = to_html(fig, full_html=False)
            elif preset == "quarterly":
                result = deals_by_quarter_with_fallback(deals_df)
                answer = str(result)
                fig = px.bar(result, x=result.index, y=result.values, title="Pipeline Value by Quarter")
                chart_html = to_html(fig, full_html=False)

        # Handle free‑text queries
        elif "query" in request.form:
            query = request.form["query"].lower()

            if "deals this quarter" in query:
                result = deals_this_quarter(deals_df)
                answer = str(result)
                try:
                    if hasattr(result, "plot"):
                        if result.__class__.__name__ == "Series":
                            fig = px.bar(result, x=result.index, y=result.values, title="Deals This Quarter")
                        else:
                            fig = px.bar(result, title="Deals This Quarter")
                        chart_html = to_html(fig, full_html=False)
                except Exception:
                    pass
            else:
                result = interpret_query(query, deals_df, work_df)
                answer = str(result)
                try:
                    if hasattr(result, "plot"):
                        if result.__class__.__name__ == "Series":
                            fig = px.bar(result, x=result.index, y=result.values, title=query)
                        else:
                            fig = px.bar(result, title=query)
                        chart_html = to_html(fig, full_html=False)
                except Exception:
                    pass

    return render_template_string(HTML_TEMPLATE, answer=answer, chart=chart_html)

if __name__ == "__main__":
    app.run(debug=True)
