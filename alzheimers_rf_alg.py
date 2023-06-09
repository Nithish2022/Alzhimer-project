import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline

sns.set()

df = pd.read_csv('oasis_longitudinal.csv')
df.head()

df = df.loc[df['Visit']==1] # use first visit data only because of the analysis we're doing
df = df.reset_index(drop=True) # reset index after filtering first visit data
df.rename(columns = {'M/F':'Gender'}, inplace = True)
df['Gender'] = df['Gender'].replace(['F','M'], [0,1]) # M/F column
df['Group'] = df['Group'].replace(['Converted'], ['Demented']) # Target variable
df['Group'] = df['Group'].replace(['Demented', 'Nondemented'], [1,0]) # Target variable
df = df.drop(['MRI ID', 'Visit', 'Hand'], axis=1) # Drop unnecessary columns

# bar drawing function
def bar_chart(feature):
    Demented = df[df['Group']==1][feature].value_counts()
    Nondemented = df[df['Group']==0][feature].value_counts()
    df_bar = pd.DataFrame([Demented,Nondemented])
    df_bar.index = ['Demented','Nondemented']
    df_bar.plot(kind='bar',stacked=True, figsize=(8,5))

# Gender  and  Group ( Female=0, Male=1)
bar_chart('Gender')
plt.xlabel('Group')
plt.ylabel('Number of patients')
plt.legend()
plt.title('Gender and Demented rate')

#MMSE : Mini Mental State Examination
# Nondemented = 0, Demented =1
# Nondemented has higher test result ranging from 25 to 30. 
#Min 17 ,MAX 30
facet= sns.FacetGrid(df,hue="Group", aspect=3)
facet.map(sns.kdeplot,'MMSE',fill= True)
facet.set(xlim=(0, df['MMSE'].max()))
facet.add_legend()
plt.xlim(15.30)

# Check missing values by each column
pd.isnull(df).sum() 
# The column, SES has 8 missing values

# Dropped the 8 rows with missing values in the column, SES
df_dropna = df.dropna(axis=0, how='any')
pd.isnull(df_dropna).sum()


df_dropna['Group'].value_counts()

# Draw scatter plot between EDUC and SES
x = df['EDUC']
y = df['SES']

ses_not_null_index = y[~y.isnull()].index
x = x[ses_not_null_index]
y = y[ses_not_null_index]

# Draw trend line in red
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
plt.plot(x, y, 'go', x, p(x), "r--")
plt.xlabel('Education Level(EDUC)')
plt.ylabel('Social Economic Status(SES)')

plt.show()

df.groupby(['EDUC'])['SES'].median()

df["SES"].fillna(df.groupby("EDUC")["SES"].transform("median"), inplace=True)

# I confirm there're no more missing values and all the 150 data were used.
pd.isnull(df['SES']).value_counts()

from sklearn.model_selection import train_test_split
#from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler 
from sklearn.model_selection import cross_val_score

# Dataset with imputation
Y = df['Group'].values # Target for the model
X = df[['Gender', 'Age', 'EDUC', 'SES', 'MMSE', 'eTIV', 'nWBV', 'ASF']] # Features we use

# splitting into three sets
X_trainval, X_test, Y_trainval, Y_test = train_test_split(
    X, Y, random_state=0)

# Feature scaling
scaler = MinMaxScaler().fit(X_trainval)
X_trainval_scaled = scaler.fit_transform(X_trainval)
X_test_scaled = scaler.transform(X_test)

# Dataset after dropping missing value rows
Y = df_dropna['Group'].values # Target for the model
X = df_dropna[['Gender', 'Age', 'EDUC', 'SES', 'MMSE', 'eTIV', 'nWBV', 'ASF']] # Features we use

# splitting into three sets
X_trainval_dna, X_test_dna, Y_trainval_dna, Y_test_dna = train_test_split(
    X, Y, random_state=0)

# Feature scaling
scaler = MinMaxScaler().fit(X_trainval_dna)
X_trainval_scaled_dna = scaler.fit_transform(X_trainval_dna)
X_test_scaled_dna = scaler.transform(X_test_dna)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score, roc_curve, auc

best_score = 0
kfolds=5
for M in range(2, 15, 2): # combines M trees
    for d in range(1, 9): # maximum number of features considered at each split
        for m in range(1, 9): # maximum depth of the tree
            # train the model
            # n_jobs(4) is the number of parallel computing
            forestModel = RandomForestClassifier(n_estimators=M, max_features=d, n_jobs=4,
                                          max_depth=m, random_state=0)
        
            # perform cross-validation
            scores = cross_val_score(forestModel, X_trainval_scaled, Y_trainval, cv=kfolds, scoring='accuracy')

            # compute mean cross-validation accuracy
            score = np.mean(scores)

            # if we got a better score, store the score and parameters
            if score > best_score:
                best_score = score
                best_M = M
                best_d = d
                best_m = m

# Rebuild a model on the combined training and validation set        
SelectedRFModel = RandomForestClassifier(n_estimators=M, max_features=d,
                                          max_depth=m, random_state=0).fit(X_trainval_scaled, Y_trainval )

PredictedOutput = SelectedRFModel.predict(X_test_scaled)
test_score = SelectedRFModel.score(X_test_scaled, Y_test)
test_recall = recall_score(Y_test, PredictedOutput, pos_label=1)
fpr, tpr, thresholds = roc_curve(Y_test, PredictedOutput, pos_label=1)
test_auc = auc(fpr, tpr)
print("Best accuracy on validation set is:", best_score)
print("Best parameters of M, d, m are: ", best_M, best_d, best_m)
print("Test accuracy with the best parameters is", test_score)
print("Test recall with the best parameters is:", test_recall)
print("Test AUC with the best parameters is:", test_auc)

'''# Inference on user input
Gender = input("Enter your gender (0 for female, 1 for male): ")
Age = input("Enter your age: ")
EDUC = input("Enter the years of education: ")
SES = input("Enter your socioeconomic status: ")
MMSE = input("Enter your mini mental state examination mark: ")
eTIV = input("Enter your estimated total intacranial volume: ")
nWBV = input("Enter your normalize whole brain volume: ")
ASF = input("Enter your atlas scaline factor value: ")'''

import tkinter as tk
import pandas as pd

# Create the main window
root = tk.Tk()

# Set the window title
root.title("Input Dialog")

# Create 8 labels and entry boxes
label1 = tk.Label(root, text="Gender:")
entry1 = tk.Entry(root)
label2 = tk.Label(root, text="Age:")
entry2 = tk.Entry(root)
label3 = tk.Label(root, text="EDUC:")
entry3 = tk.Entry(root)
label4 = tk.Label(root, text="SES:")
entry4 = tk.Entry(root)
label5 = tk.Label(root, text="MMSE:")
entry5 = tk.Entry(root)
label6 = tk.Label(root, text="eTIV:")
entry6 = tk.Entry(root)
label7 = tk.Label(root, text="nWBV:")
entry7 = tk.Entry(root)
label8 = tk.Label(root, text="ASF:")
entry8 = tk.Entry(root)

# Position the labels and entry boxes using the grid layout
label1.grid(row=0, column=0, sticky="E")
entry1.grid(row=0, column=1)
label2.grid(row=1, column=0, sticky="E")
entry2.grid(row=1, column=1)
label3.grid(row=2, column=0, sticky="E")
entry3.grid(row=2, column=1)
label4.grid(row=3, column=0, sticky="E")
entry4.grid(row=3, column=1)
label5.grid(row=4, column=0, sticky="E")
entry5.grid(row=4, column=1)
label6.grid(row=5, column=0, sticky="E")
entry6.grid(row=5, column=1)
label7.grid(row=6, column=0, sticky="E")
entry7.grid(row=6, column=1)
label8.grid(row=7, column=0, sticky="E")
entry8.grid(row=7, column=1)




'''user_prediction = SelectedRFModel.predict(inputuser)
if user_prediction== 1:
    ans="DEMENTED"
else:
    ans="NON-DEMENTED"'''
    
def display_inputs():
    # Create a function to display the inputs
    # Get the values from the entry boxes
    Gender = entry1.get()
    Age = entry2.get()
    EDUC = entry3.get()
    SES = entry4.get()
    MMSE = entry5.get()
    eTIV = entry6.get()
    nWBV = entry7.get()
    ASF = entry8.get()
    # Create a Pandas dataframe to store the inputs
    data = {'Gender': [Gender], 'Age': [Age], 'EDUC': [EDUC], 'SES': [SES], 'MMSE': [MMSE], 'eTIV': [eTIV], 'nWBV': [nWBV], 'ASF': [ASF]}
    inputuser = pd.DataFrame(data)
    inputuser.head()
    inputs_label = tk.Label(root, text=f"Input Values: {Gender}, {Age}, {EDUC}, {SES}, {MMSE}, {eTIV}, {nWBV}, {ASF}")
    inputs_label.grid(row=8, column=20)
   
# Create a function to display the dataframe
def show_results():
        # Do some processing on the dataframe
        # ...
        # Predict target variable for user input
        
        # Create a label to display the results
    #user_prediction = SelectedRFModel.predict(inputuser)
    if user_prediction== 1:
        ans="DEMENTED"
    else:
        ans="NON-DEMENTED"    
    label = tk.Label(root, text=ans)
    label.grid(row=10, column=0)
   
    
# Create a button to show the results
button = tk.Button(root, text="Show Results", command=show_results)
button.grid(row=10, column=0)

# Create a button to display the inputs
button = tk.Button(root, text="Display Inputs", command=display_inputs)
button.grid(row=8, column=0)


    
# Run the main loop
root.mainloop()



# Convert user input to a DataFrame
#user_input = pd.DataFrame({'Gender': [Gender], 'Age': [Age], 'EDUC': [EDUC], 'SES': [SES], 'MMSE': [MMSE], 'eTIV': [eTIV], 'nWBV': [nWBV], 'ASF': [ASF]})

# Convert categorical variables to dummy variables
#user_input = pd.get_dummies(df)

# Predict target variable for user input
user_prediction = SelectedRFModel.predict(user_input)

if user_prediction == 1:
  print("DEMENTED")
else:
  print("NON-DEMENTED")

#m = 'Random Forest'
#2acc.append([m, test_score, test_recall, test_auc, fpr, tpr, thresholds])


