from divtools.common.model import Model
from typing import List, Callable, Tuple


def accumulate_by_coefficients(functions: List[Tuple[Callable, float]], objects: List[Model]) -> float:
    result = 0
    for function, coefficient in functions:
        result += function(objects) * coefficient
    return result
