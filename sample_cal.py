from divtools.model.game_level_2d import GameLevel2D
from divtools.model.game_trace_2d import GameOperationSequence
from divtools.diversity.average import average_of_difference,average_of_value
from divtools.common.utils import calculate_average_vertical_distance,calculate_linear_regression_least_squares

import logging
logger= logging.getLogger(__name__)


sample_level1=GameLevel2D(list([list([1,2,3]),list([2,3,4])]))
sample_level2=GameLevel2D(list([list([1,2,3]),list([2,3,6])]))
sample_level3=GameLevel2D(list([list([1,2,3]),list([2,3,4])]))

level_set1=[sample_level1,sample_level2]
level_set2=[sample_level1,sample_level3]
level_set3=[sample_level1,sample_level2,sample_level3]

try:
    GameLevel2D.calculate_leniency(sample_level1,{1:1,2:2,3:3},allow_undefined=False)
except Exception as e:
    logger.warning(f"e:{e}")
    
dict= {1:1,2:2,3:3}
    
print(GameLevel2D.calculate_leniency(sample_level1,{1:1,2:2,3:3}))
    
    
print(GameLevel2D.calculate_linearity(sample_level1,{1:1,2:2,3:3,4:0},calculate_average_vertical_distance))
print(GameLevel2D.calculate_linearity(sample_level1,{1:1,2:2,3:3,4:0},calculate_linear_regression_least_squares))
    
print(GameLevel2D.calculate_leniency(sample_level1,{1:1,2:2,3:3,4:4},allow_undefined=False))







trace1 = GameOperationSequence([(0,1),(1,2),(2,3)])
trace2 = GameOperationSequence([(0,1),(2,3),(1,2)])
trace3 = GameOperationSequence([(0,1),(1,3),(2,2)])
trace4 = GameOperationSequence([(0,1),(1,3),(2,2),(3,3)])
trace5 = GameOperationSequence([(0,0),(1,0),(2,0),(3,0),(4,0)])


trace_set1=[trace1,trace2,trace3,trace4,trace5]
print(average_of_difference(GameOperationSequence.calculate_minimum_edit_distance)(trace_set1))