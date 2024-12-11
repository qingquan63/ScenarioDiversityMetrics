
from divtools.common.select import select_topk_objs,select_topk_objs_with_distance
from divtools.common.model import Model
from typing import List

class Test_distance():
    def test_select_topk_objs(self):
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
        
        center_point=Point(1,1.2)
        points=[Point(0,0),Point(1,0),Point(0,1),Point(1,2),Point(5,5)]
        result:List[Point]=select_topk_objs(objs=points,k=1,center_obj=center_point,distance_fn=distance_fn)
        assert result==[Point(1,2)]
        result:List[Point]=select_topk_objs(objs=points,k=2,center_obj=center_point,distance_fn=distance_fn)
        assert result==[Point(1,2),Point(0,1)]
        result:List[Point]=select_topk_objs(objs=points,k=3,center_obj=center_point,distance_fn=distance_fn)
        assert result==[Point(1,2),Point(0,1),Point(1,0)]
    
    
    def test_select_topk_objs_with_distance(self):
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
        
        center_point=Point(1,1.2)
        points=[Point(0,0),Point(1,0),Point(0,1),Point(1,2),Point(5,5)]
        result=select_topk_objs_with_distance(objs=points,k=3,center_obj=center_point,distance_fn=distance_fn)
        assert result==[(Point(1,2),distance_fn(Point(1,2),center_point)),
                        (Point(0,1),distance_fn(Point(0,1),center_point)),
                        (Point(1,0),distance_fn(Point(1,0),center_point))]