




import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, log_loss
from sklearn import tree
from sklearn import linear_model
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
import sys,os

data = pd.read_csv(sys.argv[1],header = None,names = ['buying','maint','doors','persons','lug_boot','safety','cat'])


print "\n"
print "DATA Info::"
print data.info()





data['buying'] = data['buying'].map({'vhigh' : 3,'high' : 2, 'med' : 1, 'low' : 0})
data['maint'] = data['maint'].map({'vhigh' : 3,'high' : 2, 'med' : 1, 'low' : 0})
data['doors'] = data['doors'].map({'5more' : 5, '2' : 2,'3' : 3, '4' : 4})
data['persons'] = data['persons'].map({'more' : 5, '2' : 2, '4' : 4})
data['lug_boot'] = data['lug_boot'].map({'small' : 0,'med' : 1, 'big' : 2})
data['safety'] = data['safety'].map({'low' : 0,'med' : 1, 'high' : 2})
data['cat'] = data['cat'].map({'unacc' : 0,'acc' : 1,'good' : 2,'vgood' : 3})



train =data.sample(frac = 0.7)
test = data.loc[~data.index.isin(train.index)]





x_train = train[train.columns[0:6]]
y_train  = train[train.columns[6]]
x_test = test[test.columns[0:6]]
y_test = test[test.columns[6]]




classifiers = {}
clf = tree.DecisionTreeClassifier()
clf.set_params(max_leaf_nodes = 50,max_depth = 10, max_features = None)
dt_clf = clf.fit(x_train,y_train)
dt_predict = dt_clf.predict(x_test)
dt_acc = accuracy_score(y_test,dt_predict)
param =  dt_clf.get_params()


classifiers["DT"]=clf




clf = linear_model.Perceptron()
clf.set_params(n_iter = 15,alpha = 0.01)
pt_clf = clf.fit(x_train,y_train)
pt_predict = pt_clf.predict(x_test)
pt_acc = accuracy_score(y_test,pt_predict)


classifiers["PT"]=clf


clf = MLPClassifier()
clf.set_params(hidden_layer_sizes =(100,100), max_iter = 100,alpha = 0.3, momentum = 0.7)
nn_clf = clf.fit(x_train,y_train)
nn_predict = nn_clf.predict(x_test)
nn_acc = accuracy_score(y_test,nn_predict)


classifiers["NN"]=clf

clf = MLPClassifier()
clf.set_params(hidden_layer_sizes =(100,100,100,100), max_iter = 100,alpha = 0.3, momentum = 0.7,activation = "relu")
nn_clf = clf.fit(x_train,y_train)
nn_predict = nn_clf.predict(x_test)
nn_acc = accuracy_score(y_test,nn_predict)

classifiers["DNN"]=clf

clf = svm.SVC()
clf.set_params(C = 100, kernel = "rbf")
svm_clf = clf.fit(x_train,y_train)
svm_predict = svm_clf.predict(x_test)
svm_acc = accuracy_score(y_test,svm_predict)

classifiers["SVM"]=clf




clf = MultinomialNB()
clf.set_params(alpha = 1)
nb_clf = clf.fit(x_train,y_train)
nb_predict = nb_clf.predict(x_test)
nb_acc = accuracy_score(y_test,nb_predict)

classifiers["NB"]=clf


# In[303]:

clf = LogisticRegression()
clf.set_params(C = 10, max_iter = 10)
lr_clf = clf.fit(x_train,y_train)
lr_predict = lr_clf.predict(x_test)
lr_acc = accuracy_score(y_test,lr_predict)


classifiers["LR"]=clf


# In[304]:

clf = KNeighborsClassifier()
clf.set_params(n_neighbors= 5,leaf_size = 30)
knn_clf = clf.fit(x_train,y_train)
knn_predict = knn_clf.predict(x_test)
knn_acc = accuracy_score(y_test,knn_predict)
param =  knn_clf.get_params()


classifiers["KNN"]=clf


# In[305]:

clf = BaggingClassifier()
clf.set_params(n_estimators = 30,max_samples = 1000)
bg_clf = clf.fit(x_train,y_train)
bg_predict = bg_clf.predict(x_test)
bg_acc = accuracy_score(y_test,bg_predict)


classifiers["BG"]=clf



# In[306]:

clf = RandomForestClassifier()
clf.set_params(n_estimators = 100, max_depth = 10)
rf_clf = clf.fit(x_train,y_train)
rf_predict = rf_clf.predict(x_test)
rf_acc = accuracy_score(y_test,rf_predict)


classifiers["RF"]=clf


# In[307]:

clf = AdaBoostClassifier()
clf.set_params(n_estimators = 10, learning_rate = 1)
ada_clf = clf.fit(x_train,y_train)
ada_predict = ada_clf.predict(x_test)
ada_acc = accuracy_score(y_test,ada_predict)

classifiers["ADA"]=clf




clf = GradientBoostingClassifier()
clf.set_params(n_estimators = 30,learning_rate = 1)
gb_clf = clf.fit(x_train,y_train)
gb_predict = gb_clf.predict(x_test)
gb_acc = accuracy_score(y_test,gb_predict)


classifiers["GB"]=clf


# In[314]:
print "\n"
print " FINAL ACCURACY and F-SCORES"
print "\n"
print "Classifier -","accuracy","        ","F-score"
for clf in classifiers.values():
    accuracy = cross_val_score(clf, x_train , y_train, cv=10,scoring = 'accuracy')
    f_score = cross_val_score(clf, x_train , y_train, cv=10,scoring = 'f1_micro')
    for i in classifiers:
        if classifiers[i]== clf:
            print i,
            break
    print  " : ",accuracy.mean(), "  ",f_score.mean()


# In[ ]:



