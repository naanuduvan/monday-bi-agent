import pandas as pd

# Define your column IDs here
CLOSE_DATE_COL = "date_mm5netwn"      # Close Date (A)
STATUS_COL = "color_mm5n1c4g"         # Deal Status
SECTOR_COL = "color_mm5nrjez"         # Sector/service
EXECUTION_COL = "color_mm5n56as"      # Execution Status (Work Orders)
VALUE_COL = "numeric_mm5n112n"        # Masked Deal value

# Total pipeline value across all deals
def total_pipeline_value(df):
    if VALUE_COL not in df.columns:
        return 0
    return round(df[VALUE_COL].sum(), 2)

# Count of open deals
def open_deals(df):
    if STATUS_COL not in df.columns:
        return 0
    return len(df[df[STATUS_COL] == "Open"])

# Count of won deals
def won_deals(df):
    if STATUS_COL not in df.columns:
        return 0
    return len(df[df[STATUS_COL] == "Won"])

# Deals grouped by sector
def sector_summary(df):
    if SECTOR_COL not in df.columns:
        return pd.Series(dtype=int)
    return df[SECTOR_COL].value_counts()

# Execution status summary
def execution_summary(df):
    if EXECUTION_COL not in df.columns:
        return pd.Series(dtype=int)
    return df[EXECUTION_COL].value_counts()

# Deals closing in the current quarter
def deals_this_quarter(df):
    if CLOSE_DATE_COL not in df.columns:
        return pd.DataFrame()

    df[CLOSE_DATE_COL] = pd.to_datetime(df[CLOSE_DATE_COL], errors="coerce")
    current_quarter = pd.Period(pd.Timestamp.today(), freq="Q")

    return df[df[CLOSE_DATE_COL].dt.to_period("Q") == current_quarter]

# Deals by sector for current quarter
def deals_by_sector_this_quarter(df, sector):
    if CLOSE_DATE_COL not in df.columns or SECTOR_COL not in df.columns:
        return pd.DataFrame()

    df[CLOSE_DATE_COL] = pd.to_datetime(df[CLOSE_DATE_COL], errors="coerce")
    current_quarter = pd.Period(pd.Timestamp.today(), freq="Q")

    return df[
        (df[CLOSE_DATE_COL].dt.to_period("Q") == current_quarter) &
        (df[SECTOR_COL] == sector)
    ]

# Pipeline value by sector for current quarter
def sector_value_this_quarter(df):
    if CLOSE_DATE_COL not in df.columns or SECTOR_COL not in df.columns or VALUE_COL not in df.columns:
        return pd.Series(dtype=float)

    df[CLOSE_DATE_COL] = pd.to_datetime(df[CLOSE_DATE_COL], errors="coerce")
    current_quarter = pd.Period(pd.Timestamp.today(), freq="Q")

    quarter_df = df[df[CLOSE_DATE_COL].dt.to_period("Q") == current_quarter]
    return quarter_df.groupby(SECTOR_COL)[VALUE_COL].sum().round(2)

# Pipeline value grouped by quarter (with fallback)
def deals_by_quarter_with_fallback(df):
    if CLOSE_DATE_COL not in df.columns or VALUE_COL not in df.columns:
        return pd.Series(dtype=float)

    df[CLOSE_DATE_COL] = pd.to_datetime(df[CLOSE_DATE_COL], errors="coerce")
    df["Quarter"] = df[CLOSE_DATE_COL].dt.to_period("Q").astype(str).fillna("No Date")
    return df.groupby("Quarter")[VALUE_COL].sum().round(2)
