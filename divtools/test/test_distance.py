import pytest
from divtools.common.distance import calculate_minimum_edit_distance,calculate_constraint_minimum_edit_distance

def  test_case1():
    print("sample test case")

class Test_distance():
    def test_calculate_minimum_edit_distance(self):
        trace1 = [1,2,3]
        trace2 = [1,3,2]
        trace3 = [1,3,2]
        trace4 = [1,3,2,3]

        def difference_fn(obj1,obj2):
            return 1 if obj1!=obj2 else 0
        
        assert calculate_minimum_edit_distance(trace1,trace2,difference_fn)==2
        assert calculate_minimum_edit_distance(trace2,trace3,difference_fn)==0
        assert calculate_minimum_edit_distance(trace2,trace4,difference_fn)==1

    def test_calculate_constraint_minimum_edit_distance(self):
        
        trace1 = [1,2,3]
        trace2 = [0,0,3,3,3,2,3]

        def difference_fn(obj1,obj2):
            return 1 if obj1!=obj2 else 0
        # print(calculate_minimum_edit_distance(trace1,trace2,difference_fn))
        assert calculate_constraint_minimum_edit_distance(trace1,trace2,difference_fn,limit=1)==6
    