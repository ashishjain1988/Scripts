import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns;

np.random.seed(0)
sns.set()
#column_labels = list('ABCD')
#row_labels = list('WXYZ')

x = ['E9.5 Male', 'E9.5 Female', 'E9.5 TGC', 'In Vitro TGC', 'E7.5 Whole', 'E9.5 Whole', 'E14.5 Whole', 'In Vitro TSC']
y = ['E9.5 Male', 'E9.5 Female', 'E9.5 TGC', 'In Vitro TGC', 'E7.5 Whole', 'E9.5 Whole', 'E14.5 Whole', 'In Vitro TSC']
#y = ['In Vitro TSC', 'E14.5 Whole','E9.5 Whole', 'E7.5 Whole', 'In Vitro TGC', 'E9.5 TGC', 'E9.5 Female', 'E9.5 Male']

#x = ['E9.5 Male', 'E9.5 Female', 'E9.5 TGC']
#y = ['E9.5 Male', 'E9.5 Female', 'E9.5 TGC']

fig, ax = plt.subplots()
#fig.suptitle('Placenta Equally Expressed Genes', fontsize=20)
fig.suptitle('Placental Differentially Expressed Genes', fontsize=20)
#fig.suptitle('Placental DEGs expressed in both studies (HE/LE)', fontsize=20)
#fig.suptitle('Placental DEGs ON/OFF', fontsize=20)
#plt.ylabel('Highly Expressed Genes')
#plt.xlabel('Low Expressed Genes')
#plt.ylabel('Genes Count ON')
#plt.xlabel('Genes Count OFF')
#data = pd.read_csv(open("/home/jain/heatmap_test_data.csv"), index_col=0)
data = np.genfromtxt('/home/jain/Diff_Gene_Exp_Matrix.csv', delimiter=',')
#ax = sns.heatmap(data, annot=True)
heatmap = plt.pcolor(data,cmap=plt.cm.Blues, alpha=0.8)
plt.colorbar(heatmap)
print data

ax.set_yticks(np.arange(data.shape[0])+0.5, minor=False)
ax.set_xticks(np.arange(data.shape[1])+0.5, minor=False)
#Labelling the groups of the heatmap
ax.set_xticklabels(x)
ax.set_yticklabels(y)
#Labelling the heatmap with the Exact values.
for y in range(data.shape[0]):
    for x in range(data.shape[1]):
        plt.text(x + 0.5, y + 0.5, '%d' % data[y, x],
                 horizontalalignment='center',
                 verticalalignment='center',
                 )

plt.show()