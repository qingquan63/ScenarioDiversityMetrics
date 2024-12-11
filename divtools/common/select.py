from typing import Set,List,Iterable,Callable,Tuple
from divtools.common.model import Model



def select_topk_objs(objs:List[Model],k:int,center_obj:Model,distance_fn:Callable) -> List[Model]:
    result=[]
    for obj in objs:
        result.append((obj,distance_fn(obj,center_obj)))
    result=sorted(result,key=lambda item: item[1])
    answer=[]
    for i in range(min(k,len(result))):
        answer.append(result[i][0])
    return answer


def select_topk_objs_with_distance(objs:List[Model],k:int,center_obj:Model,distance_fn:Callable) -> List[Tuple[Model,float]]:
    result=[]
    for obj in objs:
        result.append((obj,distance_fn(obj,center_obj)))
    result=sorted(result,key=lambda item: item[1])
    answer=[]
    for i in range(min(k,len(result))):
        answer.append(result[i])
    return answer

