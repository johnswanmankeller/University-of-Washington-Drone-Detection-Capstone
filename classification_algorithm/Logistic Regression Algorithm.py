#!/usr/bin/env python
# coding: utf-8

# In[71]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn

from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

sim = pd.read_csv("sim.csv")
print(sklearn.__version__)


# In[72]:


for index, row in sim.iterrows():
    if row.drone == 0:
        terrestrial_dRSRP.append(row.dRSRP) 
        terrestrial_RSSI.append(row.RSSI)
    else:
        drone_dRSRP.append(row.dRSRP) 
        drone_RSSI.append(row.RSSI)
        
#for index, row in sim.iterrows():
#    if row.altitude == (range of meters):
#       range_of_meters.append(row.dRSRP) 
#       range_of_meters.append(row.RSSI)
#    else:
#        range_of_meters.append(row.dRSRP) 
#        range_of_meters.append(row.RSSI)


# In[73]:


plt.xlabel('ΔRSRP')
plt.ylabel('RSSI')
ax = plt.gca()
ax.scatter(drone_dRSRP, drone_RSSI, color="b", label = 'drone')
ax.scatter(terrestrial_dRSRP, terrestrial_RSSI, color="r", label = 'terrestrial')
ax.legend()

#plt.xlabel('ΔRSRP')
#plt.ylabel('RSSI')
#ax = plt.gca()
#ax.scatter(drone_dRSRP, drone_RSSI, color="b", label = '10 - 15 meters e.g.')
#ax.scatter(terrestrial_dRSRP, terrestrial_RSSI, color="r", label = '200 - 300 meters e.g.')
#ax.legend()


# In[13]:


y = sim.drone.copy()
X = sim.drop(['drone'], axis=1)
features = sim.columns
features = list(features.drop(['drone']))


# In[14]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=123)


# In[15]:


model = LogisticRegression()
model.fit(X_train, y_train)


# In[16]:


y_pred = pd.Series(model.predict(X_test))
y_test = y_test.reset_index(drop=True)
z = pd.concat([y_test, y_pred], axis=1)
z.columns = ['True', 'Prediction']


# In[17]:


print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
print("Precision:", metrics.precision_score(y_test, y_pred))
print("Recall:", metrics.recall_score(y_test, y_pred))


# In[74]:


print(model.predict_proba(X_test))
importance = model.coef_[0]
for i,v in enumerate(importance):
	print('Feature: %s: , Score: %0.5f' % (features[i],v))
# plot feature importance
plt.bar(features, importance)
plt.ylabel('Importance')
plt.show()


# In[84]:


cnf_matrix = metrics.confusion_matrix(y_test, y_pred)

labels = [0, 1]
fig, ax = plt.subplots()
tick_marks = np.arange(len(labels))
plt.xticks(tick_marks, labels)
plt.yticks(tick_marks, labels)
# create heatmap
sns.heatmap(cnf_matrix, annot=True, cmap="YlGnBu", fmt='g')
ax.set_ylim([0,2])
plt.title('Confusion matrix', y=1.1)
plt.ylabel('True')
plt.xlabel('Predicted')


# In[ ]:




