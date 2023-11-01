import numpy as np
from GameSettings import Vector

# vel1 = np.array([10,0])
# mass1 = 1
# vel2 = np.array([-1,0])
# mass2 = 100000000

# outVel1 = (mass1 * vel1 - mass2 * vel1 + 2 * mass2 * vel2)/(mass1 + mass2)
# outVel2 = (mass2 * vel2 - mass1 * vel2 + 2 * mass1 * vel1)/(mass1 + mass2)

# print(outVel1, outVel2)

c = Vector.scalerProject(np.array([100000,0]), np.array([1,1]))

print(c)