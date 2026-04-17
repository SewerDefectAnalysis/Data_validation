def evaluate_rule_change(df_before, df_after, column, df_cctv, change_type="to_nan"):
    """
    Evaluates how many pipes were changed or deleted based on a rule,
    and how many of those have CCTV.

    Parameters:
    - df_before: DataFrame before applying the rule
    - df_after: DataFrame after applying the rule
    - column: name of the column to compare (not required for 'deleted_rows')
    - df_cctv: DataFrame with pipes that have CCTV
    - change_type: type of change. Options: "to_nan", "value_change", "deleted_rows"

    Returns:
    - total_changed: number of affected rows
    - changed_with_cctv: number of affected rows with CCTV
    - df_changed: DataFrame with affected rows (only returned if applicable)
    """

    cctv_keys = set(df_cctv['Pipe_ID'])

    if change_type == "to_nan":
        changed_mask = df_before[column].notna() & df_after[column].isna()
        df_changed = df_after[changed_mask]
        modified_keys = set(df_changed['Pipe_ID'])
        changed_with_cctv = len(modified_keys & cctv_keys)
        return len(modified_keys), changed_with_cctv

    elif change_type == "value_change":
        changed_mask = df_before[column] != df_after[column]
        df_changed = df_after[changed_mask]
        modified_keys = set(df_changed['Pipe_ID'])
        changed_with_cctv = len(modified_keys & cctv_keys)
        return len(modified_keys), changed_with_cctv

    elif change_type == "deleted_rows":
        keys_before = len(df_before)
        keys_after = len(df_after)
        deleted_keys = keys_before - keys_after
        modified_keys = deleted_keys
        changed_with_cctv = 0 #Is not possible to identify because we don't have COMPKEY
        return modified_keys, changed_with_cctv

    else:
        raise ValueError("Unsupported change type. Use 'to_nan', 'value_change', or 'deleted_rows'.")
