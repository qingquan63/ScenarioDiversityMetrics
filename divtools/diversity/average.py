from divtools.common.model import Model
from typing import List


def average_of_difference(difference_func, *args):
    def wrapper(obj_list: List[Model]) -> float:
        found_set: List = []
        if not obj_list:
            raise ValueError("calculate diversity of empty set")
        if len(obj_list) == 1:
            raise ValueError("calculate diversity of one object")

        difference_sum = 0
        for obj in obj_list:
            for other_obj in found_set:
                difference_sum += difference_func(obj, other_obj, *args)
            found_set.append(obj)

        return difference_sum * 2 / len(obj_list) / (len(obj_list) - 1)

    return wrapper


def average_of_value(value_func, *args):
    def wrapper(obj_list: List[Model]) -> float:
        found_set: List = []
        if not obj_list:
            raise ValueError("calculate diversity of empty set")

        sum = 0
        for obj in obj_list:
            sum += value_func(obj, *args)

        return sum / len(obj_list)

    return wrapper
