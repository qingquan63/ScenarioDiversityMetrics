import numpy as np
from typing import List
import inspect
import json
import os


def match_args(func):
    sig = inspect.signature(func)

    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        return func(*bound.args, **bound.kwargs)

    return wrapper


def calculate_linear_regression_least_squares(x_list: List[float], y_list: List[float]) -> float:
    X = np.array(x_list)
    Y = np.array(y_list)

    mean_X = np.mean(X)
    mean_Y = np.mean(Y)

    numerator = np.sum((X - mean_X) * (Y - mean_Y))
    denominator = np.sum((X - mean_X) ** 2)
    slope = numerator / denominator
    intercept = mean_Y - slope * mean_X

    predicted_Y = slope * X + intercept
    residuals = Y - predicted_Y

    mse = np.mean(residuals ** 2)
    return mse


def calculate_average_vertical_distance(x_list: List[float], y_list: List[float]) -> float:
    X = np.array(x_list)
    Y = np.array(y_list)

    coe = (Y[-1] - Y[0]) / (X[-1] - X[0])
    intercept = Y[0]

    predicted_Y = coe * X + intercept
    residuals = Y - predicted_Y

    average = np.mean(abs(residuals))
    return average


def read_txt(file_path: str, mapping_rules: dict):
    rules = mapping_rules
    # read level file
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.readlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    # 创建二维list
    mapped_data = []
    for line in data:
        mapped_line = []
        for char in line.strip():
            if char in rules:
                mapped_line.append(rules[char])
            else:
                raise ValueError(f"Undefined character '{char}' does not exist in mapping rule")
        mapped_data.append(mapped_line)

    return mapped_data


def load_mapping_rules(mapping_file: str) -> dict:
    try:
        with open(mapping_file, 'r', encoding='utf-8') as f:
            rules = json.load(f)
    except FileNotFoundError:
        print("Mapping rules not find")
        return None
    return rules


def level_fill(level_path: str, fill_element: str, folder_path: str, out_name: str):
    level = []
    try:
        with open(level_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                level.append(line)
    except FileNotFoundError:
        print(f"File not found: {level_path}")

    max_length = max(len(line) for line in level)
    filled_level = [line.ljust(max_length, fill_element) for line in level]

    res = ''
    for i in range(len(filled_level) - 1):
        res += filled_level[i] + '\n'
    res += filled_level[-1]
    os.makedirs(folder_path, exist_ok=True)
    out_path = os.path.join(folder_path, out_name)
    with open(out_path, 'w') as file:
        file.write(res)
