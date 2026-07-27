from business_logic import (
    deals_this_quarter,
    deals_by_sector_this_quarter,
    sector_value_this_quarter,
    deals_by_quarter_with_fallback
)

def interpret_query(query, deals_df, work_df):
    query = query.lower()

    if "pipeline" in query and "mining" in query:
        return deals_by_sector_this_quarter(deals_df, "Mining")

    if "pipeline" in query and "this quarter" in query:
        return deals_this_quarter(deals_df)

    if "sector value" in query and "this quarter" in query:
        return sector_value_this_quarter(deals_df)

    if "quarterly trend" in query or "pipeline trend" in query:
        return deals_by_quarter_with_fallback(deals_df)

    return "Sorry, I don’t understand that question yet."
