import pytest
from typing import List
from divtools.common.cluster import nearest_better_cluster
from divtools.common.model import Model

class Test_distance():
    def test_nearest_better_cluster(self):
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
        result:List[List[Point]]=nearest_better_cluster(points=points,distance_fn=distance_fn)
        assert len(result)==2
        assert len(result[0])==4
        assert len(result[1])==1
        assert result[0]==[Point(0,0),Point(1,0),Point(0,1),Point(1,2)]
        assert result[1]==[Point(5,5)]
        
        
    def test_nearest_better_cluster_with_phi(self):
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
        result:List[List[Point]]=nearest_better_cluster(points=points,distance_fn=distance_fn,phi=0.5)

        assert len(result)==3
        assert len(result[0])==2
        assert len(result[1])==2
        assert len(result[2])==1
        assert result[0]==[Point(0,0),Point(1,0)]
        assert result[1]==[Point(0,1),Point(1,2)]
        assert result[2]==[Point(5,5)]