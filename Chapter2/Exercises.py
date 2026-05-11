import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib
from typing import Callable
import datetime
from utils import input_utils
import matplotlib.ticker as mticker
from scipy import stats

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

STOCK_DATA = get_data()

def Exercise_1():
    data: pd.DataFrame = STOCK_DATA.get("APPL")[["Date", "Close/Last"]]
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

def Exercise_2():
    data: pd.DataFrame = STOCK_DATA.get("APPL")[["Date", "Close/Last"]]
    dates: np.ndarray = np.array([datetime.datetime.strptime(date, "%m/%d/%Y") for date in data["Date"].to_numpy()])
    stock_data: np.ndarray = pd.to_numeric(data["Close/Last"].str.removeprefix("$")).to_numpy()

    linear_return: np.ndarray = np.true_divide(stock_data[1:], stock_data[:-1]) - 1
    log_linear_return: np.ndarray = np.log(1 + linear_return)

    fig, (ax1, ax2) = plt.subplots(2, 1, layout="constrained")
    ax1.plot(dates[1:], linear_return)
    ax1.set(title="Linear Return APPL")
    ax1.grid()
    ax1.grid(which="minor", color="0.9")
    ax1.xaxis.set_major_locator(matplotlib.dates.YearLocator())

    ax2.plot(dates[1:], log_linear_return)
    ax2.set(title="Log Return APPL")
    ax2.grid()
    ax2.grid(which="minor", color="0.9")
    ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))
    ax2.xaxis.set_major_locator(matplotlib.dates.YearLocator())
    fig.savefig("Chapter2/Plots/APPL Returns Exercise 2.2.png")

def Exercise_3():
    data: pd.DataFrame = STOCK_DATA.get("APPL")[["Date", "Close/Last"]]
    dates: np.ndarray = np.array([datetime.datetime.strptime(date, "%m/%d/%Y") for date in data["Date"].to_numpy()])
    stock_data: np.ndarray = pd.to_numeric(data["Close/Last"].str.removeprefix("$")).to_numpy()

    def get_volatility_left_align(stock_data: np.ndarray, k: int = 10):
        squared_return: np.ndarray = np.square(np.true_divide(stock_data[1:], stock_data[:-1]) - 1)
        volatility: np.ndarray = np.array([np.mean(squared_return[i:i+k]) for i in range(len(squared_return) - k)])
        return np.sqrt(volatility)

    def get_volatility_centered_window(stock_data: np.ndarray, k: int = 10):
        squared_return: np.ndarray = np.square(np.true_divide(stock_data[1:], stock_data[:-1]) - 1)
        volatility: np.ndarray = np.array([np.mean(squared_return[t - int(k / 2) : t + int(k / 2)]) for t in range(int(k/2), len(squared_return)+int(k/2))])
        return np.sqrt(volatility)
    
    for k in [2, 4, 6, 8, 10, 20]:
        left_volatility = get_volatility_left_align(stock_data, k)
        centered_volatility = get_volatility_centered_window(stock_data, k)
        fig, (ax1, ax2) = plt.subplots(2, 1, layout="constrained")
        ax1.plot(dates[:len(left_volatility)], left_volatility)
        ax1.set(title="Left Aligned Volatility APPL")
        ax1.grid()
        ax1.grid(which="minor", color="0.9")
        ax1.xaxis.set_major_locator(matplotlib.dates.YearLocator())

        ax2.plot(dates[:len(centered_volatility)], centered_volatility)
        ax2.set(title="Centered Volatility APPL")
        ax2.grid()
        ax2.grid(which="minor", color="0.9")
        ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.2f'))
        ax2.xaxis.set_major_locator(matplotlib.dates.YearLocator())
        fig.savefig(f"Chapter2/Plots/APPL Volatilities k = {k} 2.3.png")

def Exercise_4():
    data: pd.DataFrame = STOCK_DATA.get("APPL")[["Date", "Close/Last"]]
    dates: np.ndarray = np.array([datetime.datetime.strptime(date, "%m/%d/%Y") for date in data["Date"].to_numpy()])
    stock_data: np.ndarray = pd.to_numeric(data["Close/Last"].str.removeprefix("$")).to_numpy()
    
    def part_a():
        intervals = [i * 5 for i in range(1, 7)]
        fig, axs = plt.subplots(2, 3, figsize=(12, 8))
        for i, interval in enumerate(intervals):
            row = i // 3
            column = i % 3
            interval_stock_data = np.array([stock_data[j] for j in range(0, len(stock_data), interval)])
            stock_log_returns = np.log(interval_stock_data[1:] / interval_stock_data[:-1]) 
            interval_dates = [dates[j] for j in range(0, len(stock_data), interval)]
            axs[row, column].plot(interval_dates[1:], stock_log_returns)
            axs[row, column].set(title=f"Interval (Days) = {interval}")
            
        fig.savefig(f"Chapter2/Plots/APPL Intervals 2.4a.png")


    def part_b():
        intervals = [i * 5 for i in range(1, 7)]
        fig, axs = plt.subplots(2, 3, figsize=(14, 10))
        for i, interval in enumerate(intervals):
            row = i // 3
            column = i % 3
            interval_stock_data = np.array([stock_data[j] for j in range(0, len(stock_data), interval)])
            stock_log_returns = np.log(interval_stock_data[1:] / interval_stock_data[:-1]) 
            stats.probplot(stock_log_returns, plot=axs[row, column])
            axs[row, column].set(title=f"Interval (Days) = {interval}")
        fig.savefig(f"Chapter2/Plots/APPL Intervals 2.4b.png")

    def part_c():
        intervals = [i for i in range(1, 30)]
        fig, axs = plt.subplots(1, 2, figsize=(8, 4))
        skewnesses = np.zeros(len(intervals))
        for i, interval in enumerate(intervals):
            interval_stock_data = np.array([stock_data[j] for j in range(0, len(stock_data), interval)])
            stock_log_returns = np.log(interval_stock_data[1:] / interval_stock_data[:-1]) 
            skewnesses[i] = stats.skew(stock_log_returns)
        axs[0].plot(intervals, skewnesses)
        axs[0].set(title=f"Skewness")

        kurtoses = np.zeros(len(intervals))
        for i, interval in enumerate(intervals):
            interval_stock_data = np.array([stock_data[j] for j in range(0, len(stock_data), interval)])
            stock_log_returns = np.log(interval_stock_data[1:] / interval_stock_data[:-1]) 
            kurtoses[i] = stats.kurtosis(stock_log_returns)
        axs[1].plot(intervals, kurtoses)
        axs[1].set(title=f"Kurtosis")

        fig.savefig(f"Chapter2/Plots/APPL Intervals 2.4c.png")

    parts: dict[str, Callable] = {
        "a": part_a,
        "b": part_b,
        "c": part_c
    }

    for part, part_func in parts.items():
        print(f"Part {part}")
        part_func()

def Exercise_5():
    data: pd.DataFrame = STOCK_DATA.get("APPL")[["Date", "Close/Last"]]
    dates: np.ndarray = np.array([datetime.datetime.strptime(date, "%m/%d/%Y") for date in data["Date"].to_numpy()])
    stock_data: np.ndarray = pd.to_numeric(data["Close/Last"].str.removeprefix("$")).to_numpy()
    
    def autocorr(x):
        result = np.correlate(x, x, mode='full')
        return result[result.size // 2:]

    def part_a():
        intervals = [i * 5 for i in range(1, 7)]
        fig, axs = plt.subplots(2, 3, figsize=(14, 10))
        for i, interval in enumerate(intervals):
            row = i // 3
            column = i % 3
            interval_stock_data = np.array([stock_data[j] for j in range(0, len(stock_data), interval)])
            interval_dates = np.array([dates[j] for j in range(0, len(dates), interval)])
            stock_log_returns = np.log(interval_stock_data[1:] / interval_stock_data[:-1]) 
            axs[row, column].plot(interval_dates[1:], autocorr(stock_log_returns))
            axs[row, column].set(title=f"Interval (Days) = {interval}")
        fig.savefig(f"Chapter2/Plots/APPL Intervals 2.5a.png")

    def part_b():
        intervals = [i * 5 for i in range(1, 7)]
        fig, axs = plt.subplots(2, 3, figsize=(14, 10))
        for i, interval in enumerate(intervals):
            row = i // 3
            column = i % 3
            interval_stock_data = np.array([stock_data[j] for j in range(0, len(stock_data), interval)])
            interval_dates = np.array([dates[j] for j in range(0, len(dates), interval)])
            stock_squared_returns = np.square(interval_stock_data[1:] / interval_stock_data[:-1]) 
            axs[row, column].plot(interval_dates[1:], autocorr(stock_squared_returns))
            axs[row, column].set(title=f"Interval (Days) = {interval}")

        fig.savefig(f"Chapter2/Plots/APPL Intervals 2.5b.png")

    parts: dict[str, Callable] = {
        "a": part_a,
        "b": part_b,
    }

    for part, part_func in parts.items():
        print(f"Part {part}")
        part_func()





EXERCISES: dict[str, Callable] = {
        "Exercise_1": Exercise_1,
        "Exercise_2": Exercise_2,
        "Exercise_3": Exercise_3,
        "Exercise_4": Exercise_4,
        "Exercise_5": Exercise_5
    }


def main():
    chosen_exercises: list[Callable] = input_utils.select_from_list(list(EXERCISES.keys()), prompt="Select which Exercise", select_multiple=True)

    for exercise in [EXERCISES.get(chosen_exercise) for chosen_exercise in chosen_exercises]:
        print(exercise.__name__)
        exercise()


if __name__ == "__main__":
    pass