from divtools.common.model import Model
from typing import List, Dict, Tuple, Callable
import math
from divtools.common.utils import read_txt


class GameLevel2D(Model):
    rows: int
    columns: int
    map: List[List[int]]
    metrics: Dict
    # 父数据集，当前生成的数据的原数据集
    label: str
    # 这个段的名字
    name: str

    tile_pattern: Dict

    def __init__(self, map: List[List[int]], label: str = "", name: str = ""):
        self.map = map
        self.rows = len(map)
        self.columns = len(map[0])
        self.metrics = {}
        self.label = label
        self.name = name
        self.tile_pattern = {}



    @classmethod
    def calculate_different_elements(cls, obj1, obj2) -> int:
        if not isinstance(obj1, cls) or not isinstance(obj2, cls):
            raise ValueError(f"object is not class of {cls.__name__}")

        if (obj1.rows, obj1.columns) != (obj2.rows, obj2.columns):
            raise ValueError(f"size of game level not match")

        count = 0
        for x in range(obj1.rows):
            for y in range(obj1.columns):
                if obj1.map[x][y] != obj2.map[x][y]:
                    count += 1

        return count

    @classmethod
    def tile_based_distance(cls, obj1, obj2):
        return GameLevel2D.calculate_different_elements(obj1, obj2) / (obj2.rows * obj2.columns)

    @classmethod
    def object_distance(cls, obj1, obj2):
        if obj1.metrics.keys() != obj2.metrics.keys():
            raise ValueError("Metrics keys do not match between the two levels.")

        euclidean_distance = math.sqrt(
            sum((obj1.metrics[key] - obj2.metrics[key]) ** 2 for key in obj1.metrics.keys() & obj2.metrics.keys()))
        return euclidean_distance

    @classmethod
    def minimal_neighbor_distance(cls, objs: List, distance):
        min_distance = float('inf')  # 初始化为正无穷大
        min_pair = None

        for i in range(len(objs)):
            for j in range(i + 1, len(objs)):
                distance = distance(objs[i], objs[j])
                if distance < min_distance:
                    min_distance = distance
                    min_pair = (objs[i], objs[j])

        return min_distance, min_pair

    @classmethod
    def calculate_leniency(cls, obj, value_dict: Dict[int, float], allow_undefined: bool = True) -> float:
        if not isinstance(obj, cls):
            raise ValueError(f"object is not class of {cls.__name__}")

        result = 0
        for x in range(obj.rows):
            for y in range(obj.columns):
                if (not allow_undefined) and (value_dict.get(obj.map[x][y]) is None):
                    raise ValueError(f"object contain undefined value : {obj.map[x][y]}")
                result += value_dict.get(obj.map[x][y], 0)

        return result / obj.rows / obj.columns

    def get_barycentre(self, value_dict: Dict[int, float]) -> Tuple[List[float], List[float]]:
        def calculate_barycentre(grid: List[int], value_dict: [int, float]) -> float:
            sum = 0
            cnt = 0
            for i in range(len(grid)):
                sum += value_dict[grid[i]] * (i + 1)
                cnt += value_dict[grid[i]]
            return sum / cnt if cnt else 0

        x_barycentre = []
        y_barycentre = []
        for i in range(self.columns):
            grids = []
            for j in range(self.rows):
                grids.append(self.map[j][i])
            barycentre = calculate_barycentre(grids, value_dict)
            if barycentre:
                x_barycentre.append(i)
                y_barycentre.append(barycentre)
        return (x_barycentre, y_barycentre)

    @classmethod
    def calculate_linearity(cls, obj, value_dict: Dict[int, float], diff_func: Callable):
        if not isinstance(obj, cls):
            raise ValueError(f"object is not class of {cls.__name__}")

        x_barycentre, y_barycentre = obj.get_barycentre(value_dict)
        if not len(x_barycentre) > 1:
            # sum of weight of obj.map = 0 or only one column not empty
            return 0

        return diff_func(x_barycentre, y_barycentre)

    @classmethod
    def calculate_linearity_by_column(cls, slide_list: List, diff_func: Callable):
        result = 0
        for i in range(len(slide_list) - 1):
            result += diff_func(slide_list[i], slide_list[i + 1])
        return result

    @classmethod
    def read(cls, file_path: str, rules: dict, label: str = "", name: str = ""):
        return cls(read_txt(file_path, rules), label, name)
