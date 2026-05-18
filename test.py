import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sight_reduction as sr


print(sr.find_potential_points((23,0,'N'), (88,0), (45,30, 'N'), (0,34, 'E'), (72, 0.33*60)))
print(sr.find_potential_points((23,0,'N'), (88,0), (45,30,'N'),  (0,32, 'E'), (72, 0.33*60)))

print(sr.find_potential_points((0,0,'N'), (20,0), (1,30,'N'), (0,0,'E'), (23, 0.33*60)))
print(sr.find_potential_points((0,0, 'N'), (20,0), (1,30, 'S'), (0,0, 'E'), (23, 0.33*60)))
print(sr.find_potential_points((20,0, 'N'), (0,0), (0,0, 'S'), (0,0, 'E'), (20, 0.33*60)))
