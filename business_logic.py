import pandas as pd

# Total pipeline value across all deals
def total_pipeline_value(df):
    if "numeric_mm5n112n" not in df.columns:
        return 0
    return round(df["numeric_mm5n112n"].sum(), 2)

# Count of open deals
def open_deals(df):
    if "color_mm5n1c4g" not in df.columns:
        return 0
    return len(df[df["color_mm5n1c4g"] == "Open"])

# Count of won deals
def won_deals(df):
    if "color_mm5n1c4g" not in df.columns:
        return 0
    return len(df[df["color_mm5n1c4g"] == "Won"])

# Deals grouped by sector
def sector_summary(df):
    if "color_mm5nrjez" not in df.columns:
        return pd.Series(dtype=int)
    return df["color_mm5nrjez"].value_counts()

# Execution status summary
def execution_summary(df):
    if "color_mm5n56as" not in df.columns:
        return pd.Series(dtype=int)
    return df["color_mm5n56as"].value_counts()

# Deals closing in the current quarter
def deals_this_quarter(df):
    if "date_mm5netwn" not in df.columns:
        return pd.DataFrame()

    df["date_mm5netwn"] = pd.to_datetime(df["date_mm5netwn"], errors="coerce")
    current_quarter = pd.Period(pd.Timestamp.today(), freq="Q")

    return df[df["date_mm5netwn"].dt.to_period("Q") == current_quarter]

# Deals by sector for current quarter
def deals_by_sector_this_quarter(df, sector):
    if "date_mm5netwn" not in df.columns or "color_mm5nrjez" not in df.columns:
        return pd.DataFrame()

    df["date_mm5netwn"] = pd.to_datetime(df["date_mm5netwn"], errors="coerce")
    current_quarter = pd.Period(pd.Timestamp.today(), freq="Q")

    return df[
        (df["date_mm5netwn"].dt.to_period("Q") == current_quarter) &
        (df["color_mm5nrjez"] == sector)
    ]

# Pipeline value by sector for current quarter
def sector_value_this_quarter(df):
    if "date_mm5netwn" not in df.columns or "color_mm5nrjez" not in df.columns or "numeric_mm5n112n" not in df.columns:
        return pd.Series(dtype=float)

    df["date_mm5netwn"] = pd.to_datetime(df["date_mm5netwn"], errors="coerce")
    current_quarter = pd.Period(pd.Timestamp.today(), freq="Q")

    quarter_df = df[df["date_mm5netwn"].dt.to_period("Q") == current_quarter]
    return quarter_df.groupby("color_mm5nrjez")["numeric_mm5n112n"].sum().round(2)

# Pipeline value grouped by quarter (with fallback)
def deals_by_quarter_with_fallback(df):
    if "date_mm5netwn" not in df.columns or "numeric_mm5n112n" not in df.columns:
        return pd.Series(dtype=float)

    df["date_mm5netwn"] = pd.to_datetime(df["date_mm5netwn"], errors="coerce")
    df["Quarter"] = df["date_mm5netwn"].dt.to_period("Q").astype(str).fillna("No Date")
    return df.groupby("Quarter")["numeric_mm5n112n"].sum().round(2)
