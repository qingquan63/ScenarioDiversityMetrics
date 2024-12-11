from divtools.model.game_level_2d import GameLevel2D
from divtools.diversity.average import average_of_difference,average_of_value
from divtools.diversity.accumulate_diversity import accumulate_by_coefficients



class Test_average():
    
    def test_average_of_difference(self):
        sample_level1=GameLevel2D(list([list([1,2,3]),list([2,3,4])]))
        sample_level2=GameLevel2D(list([list([1,2,3]),list([2,3,6])]))
        sample_level3=GameLevel2D(list([list([1,2,3]),list([2,3,4])]))

        level_set1=[sample_level1,sample_level2]
        level_set2=[sample_level1,sample_level3]
        level_set3=[sample_level1,sample_level2,sample_level3]

        assert average_of_difference(GameLevel2D.calculate_different_elements)(level_set1)==1
        assert average_of_difference(GameLevel2D.calculate_different_elements)(level_set2)==0
        assert average_of_difference(GameLevel2D.calculate_different_elements)(level_set3)==2/3
        
        
    def test_average_of_value(self):
        
        sample_level1=GameLevel2D(list([list([1,2,3]),list([2,3,4])]))
        sample_level2=GameLevel2D(list([list([1,2,3]),list([2,3,3])]))
        sample_level3=GameLevel2D(list([list([1,2,3]),list([2,3,4])]))

        level_set1=[sample_level1,sample_level2]
        level_set2=[sample_level1,sample_level3]
        level_set3=[sample_level1,sample_level2,sample_level3]
        dict= {1:1,2:2,3:3}
        
        assert average_of_value(GameLevel2D.calculate_leniency,dict)(level_set1)==25/12
        assert average_of_value(GameLevel2D.calculate_leniency,dict)(level_set2)==22/12
        assert average_of_value(GameLevel2D.calculate_leniency,dict)(level_set3)==2
        
        
    def test_accumulate_by_coefficients(self):
        sample_level1=GameLevel2D(list([list([1,2,3]),list([2,3,4])]))
        sample_level2=GameLevel2D(list([list([1,2,3]),list([2,3,6])]))
        sample_level3=GameLevel2D(list([list([1,2,3]),list([2,3,4])]))

        level_set1=[sample_level1,sample_level2,sample_level3]
        dict= {1:1,2:2,3:3}
        
        functions = [(average_of_value(GameLevel2D.calculate_leniency,dict),1),
                       (average_of_difference(GameLevel2D.calculate_different_elements),2)]


        
        result=accumulate_by_coefficients(functions=functions,objects=level_set1)
        expect_result=average_of_value(GameLevel2D.calculate_leniency,dict)(level_set1)+average_of_difference(GameLevel2D.calculate_different_elements)(level_set1)*2
        assert result==expect_result
