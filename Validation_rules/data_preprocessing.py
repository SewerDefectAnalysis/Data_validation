import numpy as np
import pandas as pd

def drop_all_nan_columns(df_pipes, df_hydraulic, df_cctv, df_defects):
    """
    Removes columns that contain only NaN values from each input DataFrame.

    Parameters
    ----------
    df_pipes : pandas.DataFrame
    df_hydraulic : pandas.DataFrame
    df_cctv : pandas.DataFrame
    df_defects : pandas.DataFrame

    Returns
    -------
    tuple of pandas.DataFrame
        Cleaned DataFrames with all-NaN columns removed.
    """

    dfs = [df_pipes, df_hydraulic, df_cctv, df_defects]

    cleaned_dfs = [df.dropna(axis=1, how='all') for df in dfs]

    print("Columns with NaN values in all rows were deleted from dataframes.")

    return tuple(cleaned_dfs)

def filter_valid_defects(df_defects,def_or_fea_map):
    """
    Filters the input DataFrame to keep only valid defect rows
    based on a predefined defect/feature mapping.

    Parameters
    ----------
    df_defects : pandas.DataFrame
        Input DataFrame containing a 'Defect_code' column.
    def_or_fea_map: Dictionary with valid defects

    Returns
    -------
    pandas.DataFrame
        Filtered DataFrame containing only valid defects.
    """

    # List of valid defect codes (editable if needed)
    valid_defect_codes = [code for code, val in def_or_fea_map.items() if val == 1]

    # Create a copy to avoid modifying the original DataFrame
    df = df_defects.copy()

    # Basic cleaning: remove spaces and standardize to uppercase
    df["Defect_code"] = df["Defect_code"].str.strip().str.upper()

    # Filter only valid defects
    df = df[df["Defect_code"].isin(valid_defect_codes)]

    print(f"The features were remove. Now, df_defects has {len(df)} defects.")

    return df

def remove_uncompleted_without_defects(df_cctv, df_defects):
    """
    Removes inspections from df_cctv where:
    - Inspection_status == 'U'
    - AND the inspection has no associated defects in df_defects

    Also prints the number of removed inspections.

    Parameters
    ----------
    df_cctv : pandas.DataFrame
        CCTV inspections DataFrame (must contain 'Inspection_ID' and 'Inspection_status')
    df_defects : pandas.DataFrame
        Defects DataFrame (must contain 'Inspection_ID')

    Returns
    -------
    pandas.DataFrame
        Filtered df_cctv
    """

    # Create a copy to avoid modifying original data
    df = df_cctv.copy()

    # Get Inspection_IDs that have at least one defect
    inspections_with_defects = set(df_defects["Inspection_ID"].dropna())

    # Condition: inspections to remove
    mask_remove = (
        (df["Inspection_status"] == "U") &
        (~df["Inspection_ID"].isin(inspections_with_defects))
    )

    # Count how many inspections will be removed (unique IDs)
    removed_ids = df.loc[mask_remove, "Inspection_ID"].nunique()

    # Apply filter
    df = df[~mask_remove]

    # Print result
    print(f"{removed_ids} uncompleted inspections without defects were removed")

    return df