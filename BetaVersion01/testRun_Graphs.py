import numpy as np 
import matplotlib.pyplot as plt  

# Compute the x and y coordinates for points on a sine curve 
x = np.arange(0, 40 * np.pi, 0.1) 
y = np.sin(x) 

# Plot the points using matplotlib 
plt.plot(x, y) 
plt.title('Test Run')
plt.xlabel('Time Stamp')
plt.ylabel('Altitude')
#plt.show() 
plt.savefig('my_plot.png')