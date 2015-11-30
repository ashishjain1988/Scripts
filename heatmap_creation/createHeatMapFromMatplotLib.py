import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

column_labels = list('ABCD')
row_labels = list('WXYZ')

x = ['E9.5 Male', 'E9.5 Female', 'E9.5 TGC']
y = ['E9.5 TGC', 'E9.5 Female', 'E9.5 Male']
#data = np.random.rand(4,4)

fig, ax = plt.subplots()
data = pd.read_csv(open("/home/jain/heatmap_test_data.csv"), index_col=0)
heatmap = ax.pcolor(data,cmap=plt.cm.Blues, alpha=0.8)
print data

#nba = pd.read_csv(open("/home/jain/heatmap_test_data.csv"), index_col=0)
# put the major ticks at the middle of each cell, notice "reverse" use of dimension
#print (nba)
#nba_norm = (nba - nba.mean()) / (nba.max() - nba.min())
#nba_sort = nba_norm.sort('PTS', ascending=True)
#print nba_sort
ax.set_yticks(np.arange(data.shape[0])+0.5, minor=False)
ax.set_xticks(np.arange(data.shape[1])+0.5, minor=False)


ax.set_xticklabels(x, minor=False)
ax.set_yticklabels(y, minor=False)
plt.show()