import numpy as np
import pandas as pd

def remove_nan_pipe_id(df_pipes):
    """
    Removes pipes without ID
    """
    initial_count = len(df_pipes)

    df_pipes = df_pipes[df_pipes['Pipe_ID'].notna()]

    final_count = len(df_pipes)
    removed_count = initial_count - final_count

    print(f"{removed_count} pipes were removed due to missing Pipe_ID.")

    return df_pipes


def remove_duplicate_pipe_id(df_pipes):
    """
    Removes duplicate pipes
    """
    initial_count = len(df_pipes)

    df_pipes = df_pipes.drop_duplicates(subset=['Pipe_ID'], keep='first')

    final_count = len(df_pipes)
    removed_count = initial_count - final_count

    print(f"{removed_count} duplicate pipes were removed based on Pipe_ID.")

    return df_pipes

def clean_material_column(df_pipes):
    """
    Converts to NaN undefined or empty material values
    """
    mask = (
            df_pipes['Material'].isna() |
            df_pipes['Material'].astype(str).str.strip().eq('') |
            df_pipes['Material'].astype(str).str.strip().str.lower().isin(['undefined', 'undef'])
    )

    df_pipes.loc[mask, 'Material'] = np.nan

    return df_pipes

def filter_installation_year(row, limits_dict):
    """
    Converts to NaN installation years that are out of valid range according to the pipe material
    """
    global_min_year = 1880
    material = row.get("Material")
    year = row.get("Installation_year")

    # global rule if material not in dict
    rules = limits_dict.get(material, {"min": global_min_year})

    min_year = rules.get("min", global_min_year)
    max_year = rules.get("max", None)

    if year < min_year:
        return np.nan

    if max_year is not None and year > max_year:
        return np.nan

    return year


def reclassify_sewer_category(df, threshold_diameter=100):
    """
    Reclassifies Sewer_category from 'Transmission' to 'Local'
    for pipes with Diameter between 0 and threshold_diameter.
    """
    mask = (
        (df["Sewer_category"] == "Transmission") &
        (df["Diameter"] > 0) &
        (df["Diameter"] <= threshold_diameter)
    )

    df.loc[mask, "Sewer_category"] = "Local"

    return df

def replace_zero_diameter_with_nan(df_pipes):
    """
    Replaces Diameter values equal to 0 with NaN.
    """
    df_pipes.loc[df_pipes["Diameter"] == 0, "Diameter"] = np.nan
    return df_pipes

def set_diameter_outliers_to_nan(df, outlier_max_map):
    """
    Sets Diameter to NaN for values exceeding material-specific thresholds.
    """

    df = df.copy()

    for material, max_diam in outlier_max_map.items():
        mask = (
            (df["Material"] == material) &
            (df["Diameter"] > max_diam)
        )
        df.loc[mask, "Diameter"] = np.nan

    return df

def set_small_diameters_to_nan(df, min_diameter=100):
    """
    Sets Diameter values below a minimum threshold to NaN.
    """

    df = df.copy()

    df.loc[df["Diameter"] < min_diameter, "Diameter"] = np.nan

    return df

def set_small_pipe_length_to_nan(df, min_length=0.6):
    """
    Sets Pipe_length values below a minimum threshold to NaN.
    """

    df = df.copy()

    df.loc[df["Pipe_length"] < min_length, "Pipe_length"] = np.nan

    return df

def set_negative_slope_to_nan(df):
    """
    Sets Slope and related depth columns to NaN when Slope is negative.
    """

    df = df.copy()

    cols_to_nan = ["Slope", "UP_depth", "DW_depth", "Depth"]

    df.loc[df["Slope"] <= 0, cols_to_nan] = np.nan

    return df

def set_invalid_invert_difference_to_nan(df):
    """
    Sets slope and depth-related columns to NaN when invert difference
    is greater than pipe length.
    """

    df = df.copy()

    cols_to_nan = ["Slope", "UP_depth", "DW_depth", "Depth"]

    mask = df["Dif_invert"] > df["Pipe_length"]

    df.loc[mask, cols_to_nan] = np.nan

    return df

def set_high_slope_to_nan(df, max_slope=30):
    """
    Sets Slope and related depth columns to NaN when slope exceeds a maximum threshold.
    """

    df = df.copy()

    cols_to_nan = ["Slope", "UP_depth", "DW_depth", "Depth"]

    mask = df["Slope"] > max_slope

    df.loc[mask, cols_to_nan] = np.nan

    return df

def set_negative_depths_to_nan(df):
    """
    Sets slope and depth-related columns to NaN when Depth is negative.
    """

    df = df.copy()

    cols_to_nan = ["Slope", "UP_depth", "DW_depth", "Depth"]

    mask = df["Depth"] < 0

    df.loc[mask, cols_to_nan] = np.nan

    return df

def set_excessive_depth_to_nan(df, max_depth=15):
    """
    Sets slope and depth-related columns to NaN when Depth exceeds a maximum threshold.
    """

    df = df.copy()

    cols_to_nan = ["Slope", "UP_depth", "DW_depth", "Depth"]

    mask = df["Depth"] > max_depth

    df.loc[mask, cols_to_nan] = np.nan

    return df

def set_non_positive_flows_to_nan(df, cols=None):
    """
    Sets flow rate columns to NaN when values are <= 0.
    """

    if cols is None:
        cols = ["Dry_peak_flow_rate", "Wet_peak_flow_rate"]

    df = df.copy()

    for col in cols:
        df.loc[df[col] <= 0, col] = np.nan

    return df
