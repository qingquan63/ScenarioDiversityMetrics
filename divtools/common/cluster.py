from typing import List,Callable
from divtools.common.model import Model



class _Edge:
    u:int
    v:int
    distance:float
    def __init__(self,u:int,v:int,distance:float) -> None:
        self.u=u
        self.v=v
        self.distance=distance

class _DisjointSet:
    parent:List[int]
    def __init__(self,point_cnt:int) -> None:
        self.parent=[i for i in range(point_cnt)]
    
    def get_parent(self,point:int) -> int:
        if self.parent[point]==point:
            return point
        self.parent[point]=self.get_parent(self.parent[point])
        return self.parent[point]
    
    def union(self,u:int,v:int):
        u=self.get_parent(u)
        v=self.get_parent(v)
        if u!=v:
            self.parent[u]=v
        
def nearest_better_cluster(points:List[Model],distance_fn:Callable,phi:float=2) -> List[List[Model]]:
    n=len(points)
    if (n==0):
        return []
    if (n==1):
        return [points]
    
    # minimum spanning tree    
    distance:List[List[float]]=[[0 for i in range(n)] for j in range(n)]
    distance_sum = 0
    edges:List[_Edge]=[]
    for point in range(n-1):
        nearest_point = point + 1 
        for other_point in range(point+1,n):
            distance[point][other_point]=distance[other_point][point]=distance_fn(points[point],points[other_point])
            if distance[point][other_point]<distance[point][nearest_point]:
                nearest_point=other_point
                
        edges.append(_Edge(point,nearest_point,distance[point][nearest_point]))
        distance_sum+=distance[point][nearest_point]
    
    # delete edges 
    distance_mean=distance_sum/(len(points)-1)
    distance_limit=phi*distance_mean
    for edge in edges:
        if edge.distance>distance_limit:
            edges.remove(edge)
    
    # find connected subgraph
    disjoint_set=_DisjointSet(n)
    for edge in edges:
        disjoint_set.union(edge.u,edge.v)
    
    subgraph:List[List[Model]]=[]
    for set_index in range(n):
        point_set:List[Model]=[]
        for point in range(n):
            if disjoint_set.get_parent(point)==set_index:
                point_set.append(points[point])
        if point_set:
            subgraph.append(point_set)
    
    return subgraph