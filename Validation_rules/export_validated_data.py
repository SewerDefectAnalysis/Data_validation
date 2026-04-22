import pandas as pd

def export_dataframes_to_excel(output_path, df_pipes, df_hydraulics, df_cctv, df_defects):
    """
    Export multiple dataframes into an Excel file with separate sheets.
    """

    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        df_pipes.to_excel(writer, sheet_name="PIPES", index=False)
        df_hydraulics.to_excel(writer, sheet_name="HYDRAULIC_PROPERTIES", index=False)
        df_cctv.to_excel(writer, sheet_name="CCTV", index=False)
        df_defects.to_excel(writer, sheet_name="DEFECTS", index=False)

    print("✅ Finished successfully")