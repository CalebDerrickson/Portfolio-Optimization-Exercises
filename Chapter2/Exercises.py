import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib
from typing import Callable
import datetime
import matplotlib.ticker as mticker

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


def Exercise_1():
    data: pd.DataFrame = get_data("APPL").get("APPL")[["Date", "Close/Last"]]
    dates: np.ndarray = np.array([datetime.datetime.strptime(date, "%m/%d/%Y") for date in data["Date"].to_numpy()])
    stock_data: np.ndarray = pd.to_numeric(data["Close/Last"].str.removeprefix("$")).to_numpy()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, layout="constrained")
    ax1.plot(dates, stock_data)
    ax1.set(title="Closing Price (Linear Scale)")
    ax1.grid()
    ax1.grid(which="minor", color="0.9")
    ax1.xaxis.set_major_locator(matplotlib.dates.YearLocator())

    ax2.semilogy(dates, stock_data)
    ax2.set(title="Closing Price (Log Scale)")
    ax2.grid()
    ax2.grid(which="minor", color="0.9")
    ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))
    ax2.xaxis.set_major_locator(matplotlib.dates.YearLocator())
    fig.savefig("Chapter2/Plots/APPL Closing Price Exercise 2.1.png")


def main():
    exercises: list[Callable] = [Exercise_1]
    for exercise in exercises:
        print(exercise.__name__)
        exercise()


if __name__ == "__main__":
    pass