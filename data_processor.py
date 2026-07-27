import pandas as pd

def board_to_dataframe(items):
    rows = []
    for item in items:
        row = {"Name": item["name"]}
        for column in item["column_values"]:
            row[column["id"]] = column["text"]
        rows.append(row)

    df = pd.DataFrame(rows)

    # Replace blank strings with NA
    df.replace("", pd.NA, inplace=True)

    # Fill missing values
    df.fillna("Not Available", inplace=True)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    return df


def convert_numeric(df, columns):
    for col in columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .replace("Not Available", "0")
            )
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df
