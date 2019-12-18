import matplotlib.pyplot as plt
import numpy as np

width = 0.8

highPower   = [6351]
lowPower    = [202]

indices = np.arange(len(highPower))

plt.bar(indices, highPower, width=width, 
        color='b', label='Max Power in mW')
plt.bar([i+0.25*width for i in indices], lowPower, 
        width=0.5*width, color='r', alpha=0.5, label='Min Power in mW')

plt.xticks(indices+width/2., 
           ['T{}'.format(i) for i in range(len(highPower))] )

plt.legend()
plt.show()