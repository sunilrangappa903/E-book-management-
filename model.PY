import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import statsmodels.api as sm
from imblearn.over_sampling import SMOTE
from scipy.stats import zscore

# Load the dataset
import os
liver_df = pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "updated_indian_liver_patient_final.csv"))

# Check the first few rows of the dataset
print(liver_df.head())

# Check for missing values
print("\nMissing Values:")
print(liver_df.isnull().sum())

# Optional: Handle missing values (if any)
# liver_df = liver_df.fillna(liver_df.mean())  # Example: Fill with mean values

# Check data types
print("\nData Types:")
print(liver_df.dtypes)
liver_df = liver_df.dropna() 
# Print the column names to check the exact name of the 'Liver_Disease' column
print(liver_df.columns)


print(liver_df.isnull().sum())
# Plotting the Number of patients with liver disease vs Number of patients with no liver disease
sns.countplot(data=liver_df, x='Dataset', label='Count')
# Count the number of patients diagnosed with and without liver disease
LD, NLD = liver_df['Dataset'].value_counts()
print('Number of patients diagnosed with liver disease:', LD)
print('Number of patients not diagnosed with liver disease:', NLD)
# Plotting the Number of Male and Female patients
sns.countplot(data=liver_df, x='Gender', label='Count')
# Count the number of male and female patients
M, F = liver_df['Gender'].value_counts()
print('Number of patients that are male:', M)
print('Number of patients that are female:', F)
# Plotting patient Age vs Gender
sns.catplot(x="Age", y="Gender", hue="Dataset", data=liver_df)
# Display average Age per Dataset and Gender
liver_df[['Gender', 'Dataset', 'Age']].groupby(['Dataset', 'Gender'], as_index=False).mean().sort_values(by='Dataset', ascending=False)
# Plotting Age vs Gender
g = sns.FacetGrid(liver_df, col="Dataset", row="Gender", margin_titles=True)
g.map(plt.hist, "Age", color="red")
plt.subplots_adjust(top=0.9)
g.fig.suptitle('Disease by Gender and Age')
# Plotting Gender with Total_Bilirubin and Direct_Bilirubin
g = sns.FacetGrid(liver_df, col="Gender", row="Dataset", margin_titles=True)
g.map(plt.scatter, "Direct_Bilirubin", "Total_Bilirubin", edgecolor="w")
plt.subplots_adjust(top=0.9)
# Jointplot of Total_Bilirubin vs Direct_Bilirubin
sns.jointplot(x="Total_Bilirubin", y="Direct_Bilirubin", data=liver_df, kind="reg")
# Plotting Gender with Aspartate Aminotransferase and Alamine Aminotransferase
g = sns.FacetGrid(liver_df, col="Gender", row="Dataset", margin_titles=True)
g.map(plt.scatter, "Aspartate_Aminotransferase", "Alamine_Aminotransferase", edgecolor="w")
plt.subplots_adjust(top=0.9)
# Jointplot of Alkaline_Phosphotase vs Alamine_Aminotransferase
sns.jointplot(x="Alkaline_Phosphotase", y="Alamine_Aminotransferase", data=liver_df, kind="reg")
# Plotting Gender with Total_Protiens and Albumin
g = sns.FacetGrid(liver_df, col="Gender", row="Dataset", margin_titles=True)
g.map(plt.scatter, "Total_Protiens", "Albumin", edgecolor="w")
plt.subplots_adjust(top=0.9)
# Jointplot of Total_Protiens vs Albumin
sns.jointplot(x="Total_Protiens", y="Albumin", data=liver_df, kind="reg")
# Plotting Gender with Albumin and Albumin_and_Globulin_Ratio
g = sns.FacetGrid(liver_df, col="Gender", row="Dataset", margin_titles=True)
g.map(plt.scatter, "Albumin", "Albumin_and_Globulin_Ratio", edgecolor="w")
plt.subplots_adjust(top=0.9)
# Jointplot of Albumin_and_Globulin_Ratio vs Albumin
sns.jointplot(x="Albumin_and_Globulin_Ratio", y="Albumin", data=liver_df, kind="reg")
# Plotting Gender with Albumin_and_Globulin_Ratio and Total Protiens
g = sns.FacetGrid(liver_df, col="Gender", row="Dataset", margin_titles=True)
g.map(plt.scatter, "Albumin_and_Globulin_Ratio", "Total_Protiens", edgecolor="w")
plt.subplots_adjust(top=0.9)
