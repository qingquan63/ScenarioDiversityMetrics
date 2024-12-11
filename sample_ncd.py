import os

import numpy as np
import pygame as pg

from typing import Union, List, Dict
from itertools import product
from divtools.model.game_level_2d import GameLevel2D
from divtools.diversity import ncd

PROJ_DIR = 'C:/Users/hui/Desktop/toolbox/Toolbox-of-Content-Diversity-Metrics'


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

        pg.image.load(PROJ_DIR + f'/assets/tile-{i}.png')
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


if __name__ == '__main__':

    value_list = []
    tex_size = MarioLevel.tex_size
    data = []
    levels = []
    for i in range(1, 4):
        file_name = f'C:/Users/hui/Desktop/toolbox/Toolbox-of-Content-Diversity-Metrics/levels/original/KL/mario-{i}.txt'
        if os.path.exists(file_name):
            lvl = MarioLevel.from_txt(file_name)
            level = GameLevel2D(lvl.to_num_arr().tolist())
            """ 
            'c-i': {'X': 0, 'S': 1, '-': 2, '?': 3, 'Q': 4, 'E': 5, '<': 6,
            '>': 7, '[': 8, ']': 9, 'o': 10}
            """
            print(level.map)
            print(len(level.map))
            print(len(level.map[0]))
            levels.append(level)
    result = 0
    # for i in range(len(levels)):
    #     for j in range(i + 1, len(levels)):
    #         result +=NCD.ncd(levels[i],levels[j])
    result = NCD.ncd(levels[0],levels[1])
    print("归一化压缩距离(NCD):", result)
    result = NCD.ncd(levels[0], levels[2])
    print("归一化压缩距离(NCD):", result)
    result = NCD.ncd(levels[1], levels[2])
    print("归一化压缩距离(NCD):", result)