import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import algorithm_scripts.sight_reduction as sr


print(sr.find_potential_points((23,0), (88,0), (45,30), (0,34), (72, 0.33*60)))
print(sr.find_potential_points((23,0), (88,0), (45,30), (0,32), (72, 0.33*60)))