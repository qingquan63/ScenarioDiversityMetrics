
import math

from divtools.model.game_level_2d import GameLevel2D
from divtools.model.game_trace_2d import GameOperationSequence
from divtools.diversity.average import average_of_difference,average_of_value
from divtools.common.utils import calculate_average_vertical_distance,calculate_linear_regression_least_squares
from divtools.common.model import Model

class Test_GameLevel2D:
    def test_calculate_different_elements(self):
        sample_level1=GameLevel2D(list([list([1,2,3]),list([2,3,4])]))
        sample_level2=GameLevel2D(list([list([1,2,3]),list([2,3,6])]))
        sample_level3=GameLevel2D(list([list([1,2,3]),list([2,3,4])]))
        sample_level4=GameLevel2D(list([list([2,1,3]),list([5,3,4])]))
        
        
        assert GameLevel2D.calculate_different_elements(sample_level1,sample_level2)==1
        assert GameLevel2D.calculate_different_elements(sample_level2,sample_level1)==1
        assert GameLevel2D.calculate_different_elements(sample_level1,sample_level3)==0
        assert GameLevel2D.calculate_different_elements(sample_level2,sample_level3)==1
        
        assert GameLevel2D.calculate_different_elements(sample_level1,sample_level4)==3
        assert GameLevel2D.calculate_different_elements(sample_level2,sample_level4)==4
        assert GameLevel2D.calculate_different_elements(sample_level3,sample_level4)==3
        
    def test_calculate_leniency(self):
        sample_level1=GameLevel2D(list([list([1,2,3]),list([2,3,4])]))
        
        try:
            GameLevel2D.calculate_leniency(sample_level1,{1:1,2:2,3:3},allow_undefined=False)
            assert False
        except Exception as e:
            assert isinstance(e,ValueError)
            assert e.__str__()=="object contain undefined value : 4"
        assert math.isclose(GameLevel2D.calculate_leniency(sample_level1,{1:1,2:2,3:3}),22/12,rel_tol=1e-9, abs_tol=1e-9)
        assert GameLevel2D.calculate_leniency(sample_level1,{1:1,2:2,3:3,4:4},allow_undefined=False)==2.5
    
    def test_calculate_linearity(self):
        sample_level1=GameLevel2D(list([list([1,2,3]),list([2,3,4])]))
        assert math.isclose(GameLevel2D.calculate_linearity(sample_level1,{1:1,2:2,3:3,4:0},calculate_average_vertical_distance),4/45,rel_tol=1e-9, abs_tol=1e-9)
        assert GameLevel2D.calculate_linearity(sample_level1,{1:1,2:2,3:3,4:0},calculate_linear_regression_least_squares)!=0
    
    def test_calculate_linearity_by_column(self):
        class Point(Model):
            x:float
            y:float
            def __init__(self,x:float,y:float) -> None:
                super().__init__()
                self.x=x
                self.y=y
            def __str__(self) -> str:
                return f"({self.x}, {self.y})"
            def __eq__(self, other):
                if isinstance(other, Point):
                    return self.x == other.x and self.y==other.y
                return False
        def distance_fn(u:Point,v:Point) -> float:
            return ((u.x-v.x)**2+(u.y-v.y)**2)**0.5
        
        points=[Point(0,0),Point(1,0),Point(0,1),Point(1,2),Point(5,5)]
        result=GameLevel2D.calculate_linearity_by_column(slide_list=points,diff_func=distance_fn)
        expect_result=0
        for i in range(len(points)-1):
            expect_result+=distance_fn(points[i],points[i+1])
        assert math.isclose(result,expect_result,rel_tol=1e-9, abs_tol=1e-9)
       