"""
Sample Data Analysis Script
--------------------------
This script demonstrates basic data analysis using pandas and visualization with matplotlib.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Create sample data
np.random.seed(42)
data = {
    'age': np.random.normal(35, 10, 100).astype(int),
    'income': np.random.normal(60000, 15000, 100),
    'education_years': np.random.normal(16, 3, 100).astype(int),
    'satisfaction': np.random.normal(7, 2, 100),
    'gender': np.random.choice(['Male', 'Female'], 100),
    'department': np.random.choice(['Sales', 'Engineering', 'Marketing', 'HR', 'Finance'], 100)
}

# Create DataFrame
df = pd.DataFrame(data)

# Display basic information
print("Data Shape:", df.shape)
print("\nData Types:")
print(df.dtypes)
print("\nBasic Statistics:")
print(df.describe())

# Group by analysis
print("\nAverage Satisfaction by Department:")
dept_satisfaction = df.groupby('department')['satisfaction'].mean().sort_values(ascending=False)
print(dept_satisfaction)

# Create visualizations
plt.figure(figsize=(12, 8))

# Boxplot of income by department
plt.subplot(2, 2, 1)
sns.boxplot(x='department', y='income', data=df)
plt.title('Income Distribution by Department')
plt.xticks(rotation=45)

# Age distribution
plt.subplot(2, 2, 2)
sns.histplot(df['age'], bins=20, kde=True)
plt.title('Age Distribution')

# Scatter plot: Age vs Income with gender color
plt.subplot(2, 2, 3)
sns.scatterplot(x='age', y='income', hue='gender', data=df)
plt.title('Age vs Income by Gender')

# Satisfaction correlation heatmap
plt.subplot(2, 2, 4)
correlation = df[['age', 'income', 'education_years', 'satisfaction']].corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')

plt.tight_layout()
plt.show()

# Additional analysis
print("\nSatisfaction vs Education Years Correlation:")
corr = df['satisfaction'].corr(df['education_years'])
print(f"Correlation Coefficient: {corr:.2f}")

if corr > 0.1:
    print("There appears to be a positive correlation between education and satisfaction.")
elif corr < -0.1:
    print("There appears to be a negative correlation between education and satisfaction.")
else:
    print("There appears to be little correlation between education and satisfaction.") 