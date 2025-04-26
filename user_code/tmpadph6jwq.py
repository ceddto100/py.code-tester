# Welcome to the Python Testing Environment!
# This is a sample code to get you started.

import numpy as np
import matplotlib.pyplot as plt

# Generate some data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a simple plot
plt.figure(figsize=(8, 6))
plt.plot(x, y, 'b-', linewidth=2)
plt.title('Sine Wave')
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.grid(True)

# Display the plot
plt.show()

# Print some information
print("Hello, World!")
print("NumPy version:", np.__version__)
print("Array example:", np.random.rand(5))
