import glob
import jpype
import numpy as np
import pygame as pg
from math import ceil
from enum import Enum
from typing import Union, List, Dict
from itertools import product
from divtools.model.game_level_2d import GameLevel2D
from divtools.common.utils import calculate_linear_regression_least_squares

PROJ_DIR='d:/Desktop/Toolbox-of-Content-Diversity-Metrics'
class MarioLevel:
    tex_size = 16
    height = 14
    default_seg_width = 28
    mapping = {
        'i-c': ('X', 'S', '-', '?', 'Q', 'E', '<', '>', '[', ']', 'o'),
        'c-i': {'X': 0, 'S': 1, '-': 2, '?': 3, 'Q': 4, 'E': 5, '<': 6,
                '>': 7, '[': 8, ']': 9, 'o': 10}
    }
    empty_tiles = {'-', 'E', 'o'}
    num_tile_types = len(mapping['i-c'])
    pipe_charset = {'<', '>', '[', ']'}
    pipe_intset = {6, 7, 8, 9}
    textures = [
        
        pg.image.load(PROJ_DIR+f'/assets/tile-{i}.png')
        for i in range(num_tile_types)
    ]

    def __init__(self, content):
        if isinstance(content, np.ndarray):
            self.content = content
        else:
            tmp = [list(line) for line in content.split('\n')]
            while not tmp[-1]:
                tmp.pop()
            self.content = np.array(tmp)
        self.h, self.w = self.content.shape
        self.__tile_pttr_cnts = {}
        self.attr_dict = {}

    def to_num_arr(self):
        res = np.zeros((self.h, self.w), int)
        for i, j in product(range(self.h), range(self.w)):
            char = self.content[i, j]
            res[i, j] = MarioLevel.mapping['c-i'][char]
        return res

    def to_img(self, save_path='render.png') -> pg.Surface:
        tex_size = MarioLevel.tex_size
        num_lvl = self.to_num_arr()
        # img = Image.new('RGBA', (self.w * tex_size, self.h * tex_size), (80, 80, 255, 255))
        img = pg.Surface((self.w * tex_size, self.h * tex_size))
        img.fill((150, 150, 255))

        for i, j in product(range(self.h), range(self.w)):
            tile_id = num_lvl[i, j]
            if tile_id == 2:
                continue
            img.blit(
                MarioLevel.textures[tile_id],
                (j * tex_size, i * tex_size, tex_size, tex_size)
            )
        
        return img

    def save(self, fpath):
        # safe_path = get_path(fpath)
        with open(fpath, 'w') as f:
            f.write(str(self))

    def tile_pattern_counts(self, w=2):
        if not w in self.__tile_pttr_cnts.keys():
            counts = {}
            for i, j in product(range(self.h - w + 1), range(self.w - w + 1)):
                key = ''.join(self.content[i + x][j + y] for x, y in product(range(w), range(w)))
                count = counts.setdefault(key, 0)
                counts[key] = count + 1
            self.__tile_pttr_cnts[w] = counts
        return self.__tile_pttr_cnts[w]

    def tile_pattern_distribution(self, w=2):
        counts = self.tile_pattern_counts(w)
        C = (self.h - w + 1) * (self.w - w + 1)
        return {key: val / C for key, val in counts.items()}

    def __getattr__(self, item):
        if item == 'shape':
            return self.content.shape
        elif item == 'h':
            return self.content.shape[0]
        elif item == 'w':
            return self.content.shape[1]
        elif item not in self.attr_dict.keys():
            if item == 'n_gaps':
                empty_map1 = np.where(self.content[-1] in MarioLevel.empty_tiles, 1, 0)
                empty_map2 = np.where(self.content[-2] in MarioLevel.empty_tiles, 1, 0)
                res = len(np.where(empty_map1 + empty_map2 == 2))
                self.attr_dict['n_ground'] = res
            elif item == 'n_enemies':
                self.attr_dict['n_enemies'] = str(self).count('E')
            elif item == 'n_coins':
                self.attr_dict['n_coins'] = str(self).count('o')
            elif item == 'n_questions':
                self.attr_dict['n_questions'] = str(self).count('Q')
            elif item == 'n_empties':
                empty_map = np.where(self.content in MarioLevel.empty_tiles)
                self.attr_dict['n_questions'] = len(empty_map)
        return self.attr_dict[item]

    def __str__(self):
        lines = [''.join(line) + '\n' for line in self.content]
        return ''.join(lines)

    def __add__(self, other):
        concated = np.concatenate([self.content, other.content], axis=1)
        return MarioLevel(concated)

    def __getitem__(self, item):
        return MarioLevel(self.content[item])

    @staticmethod
    def from_num_arr(num_arr):
        h, w = num_arr.shape
        res = np.empty((h, w), str)
        for i, j in product(range(h), range(w)):
            tile_id = num_arr[i, j]
            res[i, j] = MarioLevel.mapping['i-c'][int(tile_id)]
        return MarioLevel(res)

    @staticmethod
    def from_txt(fpath):
        # safe_path = get_path(fpath)
        with open(fpath, 'r') as f:
            return MarioLevel(f.read())

    @staticmethod
    def from_one_hot_arr(one_hot_arr: np.ndarray):
        num_lvl = one_hot_arr.argmax(axis=0)
        return MarioLevel.from_num_arr(num_lvl)

    def split_long_level(self, w_size: int = 28, step: int = 28) -> List:
        res = []
        start = 0
        while start + w_size < self.w:
            res.append(MarioLevel(self.content[:, start:start + w_size]))
            start += step
        res.append(MarioLevel(self.content[:, -w_size:]))
        return res

    def split_long_level_content(self, w_size: int = 28, step: int = 28) -> List:
        res = []
        start = 0
        content = self.to_num_arr()
        while start + w_size < self.w:
            res.append(content[:, start:start + w_size])
            start += step
        res.append(content[:, -w_size:])
        return res


class MarioJavaAgents(Enum):
    Baumgarten = 'agents.robinBaumgarten'

    def __str__(self):
        return self.value + '.Agent'


class MarioProxy:
    # __jmario = jpype.JClass("MarioProxy")()

    def __init__(self):
        if not jpype.isJVMStarted():
            jpype.startJVM(
                jpype.getDefaultJVMPath() if JVMPath is None else JVMPath,
                f"-Djava.class.path={PRJROOT}Mario-AI-Framework.jar", '-Xmx1g'
            )
            """
                -Xmx{size} set the heap size.
            """
        self.__proxy = jpype.JClass("MarioProxy")()

    @staticmethod
    def __extract_res(jresult):
        return {
            'status': str(jresult.getGameStatus().toString()),
            'completing-ratio': float(jresult.getCompletionPercentage()),
            '#kills': int(jresult.getKillsTotal()),
            '#kills-by-fire': int(jresult.getKillsByFire()),
            '#kills-by-stomp': int(jresult.getKillsByStomp()),
            '#kills-by-shell': int(jresult.getKillsByShell()),
            'trace': [
                [float(item.getMarioX()), float(item.getMarioY())]
                for item in jresult.getAgentEvents()
            ],
            'behavior': [
                item.getActions() for item in jresult.getAgentEvents()
            ]
        }

    def play_game(self, level: Union[str, MarioLevel]):
        if type(level) == str:
            jfilepath = JString(level)
            jresult = self.__proxy.playGameFromTxt(jfilepath)
        else:
            jresult = self.__proxy.playGame(JString(str(level)))
        return MarioProxy.__extract_res(jresult)

    def simulate_game(self,
                      level: Union[str, MarioLevel],
                      agent: MarioJavaAgents = MarioJavaAgents.Baumgarten,
                      render: bool = False
                      ) -> Dict:
        """
        Run simulation with an agent for a given level
        :param level: if type is str, must be path of a valid level file.
        :param agent: type of the agent.
        :param render: render or not.
        :return: dictionary of the results.
        """
        # start_time = time.perf_counter()
        jagent = jpype.JClass(str(agent))()
        if type(level) == str:
            level = MarioLevel.from_txt(level)
        # real_time_limit_ms = 2 * (level.w * 15 + 1000)
        real_time_limit_ms = int(3 if not render else 5)
        jresult = self.__proxy.playGame(JString(str(level)), jagent, real_time_limit_ms, render)
        # Refer to Mario-AI-Framework.engine.core.MarioResult, add more entries if need be.
        return MarioProxy.__extract_res(jresult)

    def simulate_long_game(self,
                           level: Union[str, MarioLevel],
                           agent: MarioJavaAgents = MarioJavaAgents.Baumgarten,
                           k: float = 2., b: int = 200
                           ) -> Dict:
        # start_time = time.perf_counter()
        ts = MarioLevel.tex_size
        jagent = jpype.JClass(str(agent))()
        if type(level) == str:
            level = MarioLevel.from_txt(level)
        reached_tile = 0
        res = {'restarts': [], 'trace': []}
        dx = 0
        while reached_tile < level.w - 1:
            jresult = self.__proxy.runGame(JString(str(level[:, reached_tile:])), jagent)
            pyresult = MarioProxy.__extract_res(jresult)

            reached = pyresult['trace'][-1][0]
            reached_tile += ceil(reached / ts)
            if pyresult['status'] != 'WIN':
                res['restarts'].append(reached_tile)
            res['trace'] += [[dx + item[0], item[1]] for item in pyresult['trace']]
            dx = reached_tile * ts
        return res

    @staticmethod
    def get_seg_infos(full_info, check_points=None):
        restarts, trace = full_info['restarts'], full_info['trace']
        W = MarioLevel.default_seg_width
        ts = MarioLevel.tex_size
        if check_points is None:
            end = ceil(trace[-1][0] / ts)
            check_points = [x for x in range(W, end, W)]
            check_points.append(end)
        res = [{'trace': [], 'playable': True} for _ in check_points]
        s, e, i = 0, 0, 0
        restart_pointer = 0
        # dx = 0
        while True:
            while e < len(trace) and trace[e][0] < ts * check_points[i]:
                if restart_pointer < len(restarts) and restarts[restart_pointer] < check_points[i]:
                    res[i]['playable'] = False
                    restart_pointer += 1
                e += 1
            x0 = trace[s][0]
            res[i]['trace'] = [[item[0] - x0, item[1]] for item in trace[s:e]]
            # x0, y0 = trace[s]
            # res[i]['trace'] = [[item[0] - x0, item[1] - y0] for item in trace[s:e]]
            # dx = ts * check_points[i]
            i += 1
            if i == len(check_points):
                break
            s = e
        return res


def level_sum(lvls) -> MarioLevel:
    if type(lvls[0]) == MarioLevel:
        concated_content = np.concatenate([l.content for l in lvls], axis=1)
    else:
        concated_content = np.concatenate([l for l in lvls], axis=1)
    return MarioLevel(concated_content)


def traverse_level_files(path='levels/train'):
    for lvl_path in glob.glob(f'{path}\\*.txt'):
        lvl = MarioLevel.from_txt(lvl_path)
        name = lvl_path.split('\\')[-1][:-4]
        yield lvl, name

def save_img(img,save_path) -> None:
    # safe_path = get_path(save_path)
    pg.image.save(img, save_path)

def cal_line(x_list,y_list):
    X = np.array(x_list)
    Y = np.array(y_list)

    mean_X = np.mean(X)
    mean_Y = np.mean(Y)

    numerator = np.sum((X - mean_X) * (Y - mean_Y))
    denominator = np.sum((X - mean_X) ** 2)
    slope = numerator / denominator
    intercept = mean_Y - slope * mean_X
    return slope,intercept


BLACK=(0,0,0)
RED = (255, 0, 0)
if __name__ == '__main__':
    import os
    
    value_list=[]
    tex_size = MarioLevel.tex_size
    data=[]
    for i in range(99):
        file_name = PROJ_DIR+f'/levels/original/linearity/mario-{i}.txt'
        if os.path.exists(file_name):
            lvl = MarioLevel.from_txt(file_name)
            level=GameLevel2D(lvl.to_num_arr().tolist())
            """ 
            'c-i': {'X': 0, 'S': 1, '-': 2, '?': 3, 'Q': 4, 'E': 5, '<': 6,
            '>': 7, '[': 8, ']': 9, 'o': 10}
            """
            
            weight_dict={0:1,1:1,2:0,3:1,4:1,5:0,6:1,7:1,8:1,9:1,10:0}
            x_list,y_list=level.get_barycentre(weight_dict)
            
            img = lvl.to_img()
            # for k in range(len(x_list)):
            #     x=x_list[k]
            #     y=y_list[k]    
            #     pg.draw.circle(img,RED,(x*tex_size+tex_size/2,y*tex_size-tex_size/2),5)
            
            # k,b=cal_line(x_list,y_list)
            # st=(0,b*tex_size)
            # ed=(level.columns*tex_size,(k*level.columns+b)*tex_size)
            # pg.draw.line(img,BLACK,st,ed, 3)
            
            save_img(img,PROJ_DIR+f'/levels/original/linearity/mario-{i}.png')
            result=GameLevel2D.calculate_linearity(level,weight_dict,calculate_linear_regression_least_squares)
            value_list.append((result,i))
            data.append(result)
    value_list=sorted(value_list)
    print(value_list)
    
    import matplotlib.pyplot as plt

    # 绘制直方图
    plt.hist(data, bins=50, edgecolor='black')  # 可以调整 bins 的值来控制直方图的柱子数量
    plt.title('Linearity')
    plt.xlabel('值')
    plt.ylabel('频数')

    plt.show()
    
    
        
