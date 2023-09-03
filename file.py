# import numpy as np

for i in range(100):
    test = [float(i) for i in input().split()]
    dataset = {'x': [], 'y': []}
    det = 0
for i in range(len(test)):
  if i % 2 == 0:
    dataset['x'].append(test[i])
  else:
    dataset['y'].append(test[i])
    # det = np.linalg.det(np.cov(dataset['x'], dataset['y']))
    det += test[i]
if det < 0.045:
  print(1)
else:
  print(2)


