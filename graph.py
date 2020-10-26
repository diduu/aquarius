import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
colnames = ['R', 'G', 'B']
df = pd.read_csv('results.csv', names=colnames)
plt.figure(figsize=(30,5))
plt.grid(True)
y1 = df['R']
y2 = df['G']
y3 = df['B']
x = [i for i in range(len(y1))]
print(df)
y1.rolling(window=7).mean().plot()
plt.scatter(x, y1, color='red', s=5)
y2.rolling(window=7).mean().plot()
plt.scatter(x, y2, color='green', s=5)
y3.rolling(window=7).mean().plot()
plt.scatter(x, y3, color='blue', s=5)
# plt.xticks(df.DROPS[::10])
plt.ylabel("RGB Value")
plt.show()
