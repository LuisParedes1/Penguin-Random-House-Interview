from pandas import DataFrame, read_csv, to_datetime
from dotenv import load_dotenv
import os

def load_data() -> DataFrame:
    df = read_csv(os.getenv("DATA_PATH"), 
                     dtype={"country": "string","value": "float"}) 
    df["fecha"] = to_datetime(df["fecha"], format="%d/%m/%Y", errors="coerce")
    return df

load_dotenv()
DATASET: DataFrame = load_data()