# -*- coding: utf-8 -*-
"""CSMA121-AI and ML_coursework1_28812368

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1k0ahJ5QGhA_ZaNRAHhNPRYRBzkmAmdqc
"""

########################################Decision Tree Model###############################################

"""The Dataset described in this course work is Wisconsin Breast cancer Database.(Classification)
The model used in this is Decision tree , support vector Machine
Deep Learning( Neural Network)
"""

# Commented out IPython magic to ensure Python compatibility.
#####################################Built-in Python Libraries / Dependencies#########################################
import pandas as pd
import numpy as np
from pandas import read_csv
from google.colab import files
from sklearn.naive_bayes import MultinomialNB
import io
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import KFold 
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import confusion_matrix, plot_confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as lda
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.model_selection import cross_val_score
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
np.random.seed(123)  # for reproducibility
from matplotlib import pyplot as plt
# %matplotlib inline

# Commented out IPython magic to ensure Python compatibility.
plt.style.use('classic')
# %matplotlib inline
uploaded = files.upload()

print (uploaded['breastcancer.csv'][:200].decode('utf-8') + '...')

#To read the csv file 
df = pd.read_csv(io.StringIO(uploaded['breastcancer.csv'].decode('utf-8')))
df.columns = ['Sample code number','Clump Thickness','Uniformity of Cell Size','Uniformity of Cell Shape','Marginal Adhesion','Single Epithelial Cell Size','Bare Nuclei','Bland Chromatin','Normal Nucleoli','Mitoses','Class']
df

#First five rows of the data
df.head()

"""# **Pre-processing the Dataset**"""

# Checking the data type
df.dtypes

# Checking the missing values
df.isnull().sum()

# Dropping the duplicates 
df = df.drop_duplicates()
df

df.isna().any().sum()

#Dropping the missing values
df.drop(df.loc[df['Bare Nuclei'] == "?"].index, inplace=True)
df

#Total number of rows and columns
df.shape

#Statistics of the data dataset
df.info

"""### **Visualisation**"""

# Plotting a Histogram
ax = df['Clump Thickness'].value_counts().plot(kind='bar',figsize=(14,6))

"""The above graph plots the clump thickness of the breast cancer and  shows the various size of cells."""

# Finding the relations between the variables
plt.figure(figsize=(20,10))
c= df.corr()
sns.heatmap(c,cmap="BrBG",annot=True)

"""# The above graph sns heat map used to find the relation of the attributes. The "sample code number" with all the attributes are not correlated, whereas it does not impact much on the dataset. The "Uniformity of Cell Size" is highly correlated with 91% wheras the "Mitoses" has the correlation of 35% to 45%"""

#plot the pair plot.
sns.pairplot(df, vars=['Sample code number','Clump Thickness','Uniformity of Cell Size','Uniformity of Cell Shape','Marginal Adhesion','Single Epithelial Cell Size','Bare Nuclei','Bland Chromatin','Normal Nucleoli','Mitoses','Class'])
plt.show()

"""## **Feature Selection:**

# The dataset is having less number of attributes therefore the feature selection is not done.

## **Splitting the dataset in Target and feature**
"""

y= df.iloc[:,10]
y       #dftarget

x=df.iloc[:,0:10]
x      #dffeature

"""## **Split dataset into training set and test set**"""

#Creating the train and validation set
x_train,x_valid,y_train, y_valid = train_test_split(x,y,random_state= 1,test_size=0.3)

#Distribution in Training set
x_train.value_counts(normalize=True)

#Distribution in Validation set
y_valid.value_counts(normalize=True)

#Shape of training set
x_train.shape, y_train.shape

#Shape of Validation set
x_valid.shape, y_valid.shape

#Creating the decision tree function
classifier = DecisionTreeClassifier()

classifier=classifier.fit(x_train,y_train)

#Checking the validation score
classifier.score=(x_valid,y_valid)

#Predictions on validation set
x_predict = classifier.predict(x_valid)
metrics.accuracy_score(y_valid,x_predict)

# plotting the confusion matrix
plot_confusion_matrix(classifier,x, y)
plt.show()

"""## **Cross validation **"""

model = DecisionTreeClassifier()
# evaluate pipeline
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
scores = cross_val_score(model, x, y, scoring='roc_auc', cv=cv, n_jobs=-1)

scores

"""## Grid search k value for SMOTE oversampling  classification"""

# grid search k value for SMOTE oversampling for imbalanced classification
from numpy import mean
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.tree import DecisionTreeClassifier
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

#define dataset
x, y = make_classification(n_samples=10000, n_features=2, n_redundant=0,
	n_clusters_per_class=1, weights=[0.99], flip_y=0, random_state=1)

# values to evaluate
k_values = [1, 2, 3, 4, 5, 6, 7]
for k in k_values:
	# define pipeline
	model = DecisionTreeClassifier()
	over = SMOTE(sampling_strategy=0.1, k_neighbors=k)
	under = RandomUnderSampler(sampling_strategy=0.5)
	steps = [('over', over), ('under', under), ('model', model)]
	pipeline = Pipeline(steps=steps)
	# evaluate pipeline
	cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
	scores = cross_val_score(pipeline, x, y, scoring='roc_auc', cv=cv, n_jobs=-1)
	score = mean(scores)
	print('> k=%d, Mean ROC AUC: %.3f' % (k, score))

# borderline-SMOTE for imbalanced dataset
from collections import Counter
from sklearn.datasets import make_classification
from imblearn.over_sampling import BorderlineSMOTE
from matplotlib import pyplot
from numpy import where

# define dataset
x, y = make_classification(n_samples=10000, n_features=2, n_redundant=0,
	n_clusters_per_class=1, weights=[0.99], flip_y=0, random_state=1)

# summarize class distribution
counter = Counter(y)
print(counter)

# transform the dataset
oversample = BorderlineSMOTE()
x, y = oversample.fit_resample(x, y)

# summarize the new class distribution
counter = Counter(y)
print(counter)

# scatter plot of examples by class label
for label, _ in counter.items():
	row_ix = where(y == label)[0]
	pyplot.scatter(x[row_ix, 0], x[row_ix, 1], label=str(label))
pyplot.legend()
pyplot.show()

##################################Begining of MODEL2######################################################

"""# **Support Vector machine**"""

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 1)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

# Fitting Kernel SVM to the Training set
from sklearn.svm import SVC
classifier = SVC(kernel = 'linear', random_state = 0)
classifier.fit(x_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(x_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

cm

from sklearn.metrics import accuracy_score
accuracy=accuracy_score(y_test,y_pred)

accuracy

# Applying Grid Search to find the best model and the best parameters
from sklearn.model_selection import GridSearchCV
parameters = [{'C': [1, 10, 100, 1000], 'kernel': ['linear']},
              {'C': [1, 10, 100, 1000], 'kernel': ['rbf'], 'gamma': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]}]
grid_search = GridSearchCV(estimator = classifier,
                           param_grid = parameters,
                           scoring = 'accuracy',
                           cv = 10,
                           n_jobs = -1)
grid_search = grid_search.fit(x_train, y_train)

accuracy = grid_search.best_score_

accuracy

"""# **Grid search Parameter**"""

grid_search.best_params_

classifier = SVC(kernel = 'rbf', gamma=0.7)
classifier.fit(x_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(x_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

cm

from sklearn.metrics import accuracy_score
accuracy=accuracy_score(y_test,y_pred)

accuracy

##################################Begining of MODEL 3 ######################################################
#################################DEEP LEARNING MODEL########################################################

# Commented out IPython magic to ensure Python compatibility.
#Importing Keras Libraries#
random_state = 0from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils
from keras.datasets import mnist
from matplotlib import pyplot as plt
from sklearn.model_selection import GridSearchCV, StratifiedKFold
# %matplotlib inline

from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()
df['Class'] = labelencoder.fit_transform(df['Class'])
df

x_class=df.drop(["Class"],axis=1)
y_class=df["Class"]

from sklearn.preprocessing import StandardScaler, MinMaxScaler
#Normalise the data between 0 and 1
norma=MinMaxScaler()
x_class_scaled = norma.fit_transform(x_class)
x_class_scaled

#Creating the train and validation set
x_train,x_valid,y_train, y_valid = train_test_split(x_class_scaled,y_class,random_state= 1,test_size=0.3)

def classification_model():     
    model = Sequential()
    model.add(Dense(10, input_dim= 10, activation='relu'))
    model.add(Dense(20, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(5, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1,activation='sigmoid'))
    model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics= ['accuracy'])
    return model

from keras.wrappers.scikit_learn import KerasClassifier
estimator = KerasClassifier(build_fn=classification_model, epochs=100, batch_size=5, verbose=0)
kfold = StratifiedKFold(n_splits=10, shuffle=True)
results = cross_val_score(estimator, x_train, y_train, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))

results

##################################END of MODEL 3 ######################################################
#######################################################################################################
