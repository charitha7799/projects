import pandas as pd


def preprocess_data(df):

    df = df.copy()

    # -----------------------------------------------------
    # Replace impossible values
    # -----------------------------------------------------

    if "DAYS_EMPLOYED" in df.columns:

        df["DAYS_EMPLOYED"] = df[
            "DAYS_EMPLOYED"
        ].replace(
            365243,
            pd.NA
        )

    # -----------------------------------------------------
    # Numeric missing values
    # -----------------------------------------------------

    numeric_columns = df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    for column in numeric_columns:

        df[column] = df[column].fillna(
            df[column].median()
        )

    # -----------------------------------------------------
    # Categorical missing values
    # -----------------------------------------------------

    categorical_columns = df.select_dtypes(
        include=["object"]
    ).columns

    for column in categorical_columns:

        df[column] = df[column].fillna(
            "Unknown"
        )

    return df