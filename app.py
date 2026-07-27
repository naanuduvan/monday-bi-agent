from monday_api import get_deals, get_work_orders
from data_processor import board_to_dataframe, convert_numeric
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

print("Loading Monday.com data...\n")

# Fetch data
deals = get_deals()
work_orders = get_work_orders()

# Convert to DataFrame
deals_df = board_to_dataframe(deals)
work_df = board_to_dataframe(work_orders)

# Convert numeric columns
deals_df = convert_numeric(deals_df, ["numeric_mm5n112n"])
work_df = convert_numeric(work_df, ["numeric_mm5nc8jf", "numeric_mm5nd8vs"])

print("========== DASHBOARD ==========\n")

print("Total Pipeline Value:")
print(total_pipeline_value(deals_df))

print("\nOpen Deals:")
print(open_deals(deals_df))

print("\nWon Deals:")
print(won_deals(deals_df))

print("\nDeals by Sector:")
print(sector_summary(deals_df))

print("\nExecution Status:")
print(execution_summary(work_df))

print("\nDeals This Quarter:")
quarter_deals = deals_this_quarter(deals_df)
if quarter_deals.empty:
    print("No deals closing this quarter.")
else:
    print(quarter_deals)

print("\nMining Deals This Quarter:")
mining_deals = deals_by_sector_this_quarter(deals_df, "Mining")
if mining_deals.empty:
    print("No Mining deals closing this quarter.")
else:
    print(mining_deals)

print("\nSector Value This Quarter:")
sector_values = sector_value_this_quarter(deals_df)
if sector_values.empty:
    print("No sector values for this quarter.")
else:
    print(sector_values)

print("\nPipeline Value by Quarter (with fallback):")
quarter_values = deals_by_quarter_with_fallback(deals_df)
if quarter_values.empty:
    print("No quarterly pipeline values available.")
else:
    print(quarter_values)
    
from prompts import interpret_query

print("\n========== FOUNDER Q&A ==========\n")
sample_questions = [
    "Show me Mining pipeline this quarter",
    "What is the pipeline this quarter?",
    "Sector value this quarter",
    "Quarterly pipeline trend"
]

for q in sample_questions:
    print(f"\nQ: {q}")
    print("A:", interpret_query(q, deals_df, work_df))
