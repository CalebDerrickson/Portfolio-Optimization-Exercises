import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

PATH_TO_STORED_DATA: list[Path] = list((Path().cwd().resolve() / "Historical Data").glob("*.csv"))
STORED_DATA_NAMES = [data_path.name.split(" ")[0] for data_path in PATH_TO_STORED_DATA]

def get_data(stock_names: list[str] | str = "") -> dict[str, pd.DataFrame]:
    res: dict[str, pd.DataFrame] = dict()
    if stock_names == [] or stock_names == "":
        stock_names_to_get: set[str] = set(STORED_DATA_NAMES)
    elif isinstance(stock_names, list):
        stock_names_to_get: set[str] = {stock_name for stock_name in set(stock_names) if stock_name in STORED_DATA_NAMES}
    elif isinstance(stock_names, str):
        if stock_names not in STORED_DATA_NAMES:
            print(f"Stock name {stock_names} is not stored in data_path. The following are available: ")
            print(*STORED_DATA_NAMES, sep="\n")
            return res
        stock_names_to_get: set[str] = {stock_names}
        
    for stock_name_to_get in stock_names_to_get:
        data_path: Path = next((path for path in PATH_TO_STORED_DATA if stock_name_to_get in path.as_posix()), None)
        if data_path is None:
            continue
        res[stock_name_to_get] = pd.read_csv(data_path)

    return res
        

def main():
    stock_names = []

    stock_data: dict[str, pd.DataFrame] = get_data()
    print(stock_data.keys())


if __name__ == "__main__":
    pass