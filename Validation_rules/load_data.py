from sqlalchemy import create_engine
import pandas as pd

def load_input_data(
    source_type,
    source_path,
    sheet_names=None
):
    """
    Load input data from either a SQLite database or an Excel file.

    :param source_type: 'database' or 'excel'
    :param source_path: path to database or Excel file
    :param sheet_names: list of sheet names (required for Excel)
    :return: df_pipes, df_cctv, df_defects, df_hydraulics
    """

    df_hydraulics = None

    if source_type == "database":
        engine = create_engine(f"sqlite:///{source_path}")

        df_pipes = pd.read_sql_table("pipe", engine)
        df_cctv = pd.read_sql_table("inspection", engine)
        df_defects = pd.read_sql_table("defect", engine)

        try:
            df_hydraulics = pd.read_sql_table("hydraulic_properties", engine)
        except Exception:
            df_hydraulics = pd.DataFrame()

        print("Data loaded successfully from database")

    elif source_type == "excel":
        if sheet_names is None:
            raise ValueError("sheet_names must be provided when source_type='excel'")

        data = pd.read_excel(source_path, sheet_name=sheet_names)

        df_pipes = data.get("PIPES", pd.DataFrame())
        df_cctv = data.get("CCTV", pd.DataFrame())
        df_defects = data.get("DEFECTS", pd.DataFrame())
        df_hydraulics = data.get("HYDRAULIC_PROPERTIES", pd.DataFrame())

        print("Data loaded successfully from Excel")

    else:
        raise ValueError("source_type must be 'database' or 'excel'")

    return df_pipes, df_cctv, df_defects, df_hydraulics