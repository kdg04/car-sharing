import pandas as pd
from scipy.stats import chi2_contingency, pearsonr
from statsmodels.formula.api import ols

df = pd.read_csv('Updated_CarSharing.csv')

df = df.drop(columns=['timestamp'])         

df = df.dropna()     # Drop rows with missing values Not required if NaN values have been handled separately on previous occassion                    

# Numerical variables
numerical_variables = [ 'windspeed', 'humidity']

# Categorical variables
categorical_variables = ['season', 'holiday', 'workingday', 'temp_category', 'weather_code']

# Perform hypothesis tests
results = {}
for var in categorical_variables:
    contingency_table = pd.crosstab(df[var], df['demand'])
    chi2, p, _, _ = chi2_contingency(contingency_table)
    results[var] = {'test': 'Chi-square test', 'test_statistic': chi2, 'p-value': p}

for var in numerical_variables:
    corr, p = pearsonr(df[var], df['demand'])
    results[var] = {'test': 'Pearson correlation', 'correlation_coefficient': corr, 'p-value': p}


# Print the results
for column, result in results.items():
    print(f"Column: {column}")
    print(f"Test: {result['test']}")
    print(f"Test Statistic: {result.get('test_statistic', result.get('correlation_coefficient')):.3f}")
    print(f"P-value: {result['p-value']:.3f}")
    if result['p-value'] < 0.05:
        print("Conclusion: There is a significant relationship with demand rate.")
    else:
        print("Conclusion: There is no significant relationship with demand rate.")
    print()
