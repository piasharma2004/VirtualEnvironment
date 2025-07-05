import numpy as np
import pandas as pd

# List of names
names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Hannah', 'Ivy', 'Jack']

# Randomly choose 10 names from the list
random_names = np.random.choice(names, size=10, replace=True)

# Print the randomly chosen names
print(random_names)

# Print a message
print("Hello World")