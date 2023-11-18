import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

a=np.random.randint(1,1000,100)
b=np.random.randint(1,1000,100)
# c=np.concatenate((a,b),axis=1)

df1=pd.DataFrame(data=a,columns=['A',])
df1=pd.concat((df1,pd.DataFrame(data=b,columns=['B',])),axis=0)

dataframe=sns.load_dataset('iris')
print(dataframe)
# sns.lineplot(x='A',y='B',data=df1)
# plt.show()