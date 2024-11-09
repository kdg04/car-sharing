import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder


df = pd.read_csv('Updated_CarSharing.csv')

# encoding category variables
le = LabelEncoder()
df['temp_category_encoded'] = le.fit_transform(df['temp_category'])
df['weather_code_encoded'] = le.fit_transform(df['weather_code'])


average_demand = df['demand'].mean()                   # calculate the average demand rate

# create a new column for the labels (1 for above average, 2 for below average)
df['demand_type'] = df['demand'].apply(lambda x: 1 if x > average_demand else 2)

X = df[['temp_category_encoded', 'humidity', 'windspeed', 'weather_code_encoded']]          # Features
y = df['demand_type']                                                                          # Target variable

# split data 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=10)

# classifiers
classifiers = {
    'Logistic Regression': LogisticRegression(),
    'Support Vector Machine': SVC(),
    'Random Forest': RandomForestClassifier()
}

for name, classifier in classifiers.items():
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"{name} Accuracy: {accuracy}")