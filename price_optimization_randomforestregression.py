# -*- coding: utf-8 -*-
"""Price_Optimization_RandomForestRegression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UApgrIFB_KPYiU4jVYixlhBcBhXNFTjx
"""

import pandas as pd
import numpy as np

df = pd.read_csv('shopping_trends - Copy.csv')
df = df.drop(columns=['Color'])
df.head()

df_unseen = pd.read_csv('Testing_Scenarios - Copy.csv')
# df_unseen_data['target'] = df['Purchase_Amount']

df_unseen = df_unseen.drop(columns=['Color'])

df_unseen.head()

df_unseen.head(), len(df_unseen), len(df)

# df['target'] = df['Purchase_Amount']

df.head(10)

# Specify which columns to one-hot encode
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

categorical_cols = ['Item', 'Location', 'Season']

# Create a column transformer
# This will apply the OneHotEncoder to specified columns and leave other columns unchanged
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(), categorical_cols)
    ],
    remainder='passthrough'
)

'''preprocessor_unseen = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(), categorical_cols)
    ],
    remainder='passthrough'
)'''

# Get a list of the names of the encoded features
preprocessor.fit(df)
preprocessor.fit(df_unseen)


feature_names = preprocessor.get_feature_names_out()
feature_names_unseen = preprocessor.get_feature_names_out()

# Select the columns that we want to keep
selected_features = [feature for feature in feature_names if feature not in categorical_cols]
selected_features_unseen = [feature for feature in feature_names_unseen if feature not in categorical_cols]

# Transform the data
X_encoded = preprocessor.transform(df.drop(columns=['Purchase_Amount'])).toarray()
X_encoded_unseen = preprocessor.transform(df_unseen).toarray()

# Display the result
# print(pd.DataFrame(X_encoded, columns=selected_features))
# print(pd.DataFrame(X_encoded_unseen, columns=selected_features))

# selected_features, selected_features_unseen

len(selected_features), len(selected_features_unseen)

# feature_names, feature_names_unseen

# X_encoded.dtype, X_encoded_unseen.dtype

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 15],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Create a RandomForestRegressor
from sklearn.ensemble import RandomForestRegressor
rf_model = RandomForestRegressor(random_state=42)
rf_model.get_params()

from sklearn.model_selection import train_test_split
X_train_encoded, X_test_encoded, y_train, y_test = train_test_split(X_encoded, df['Purchase_Amount'], test_size=0.2)

# Create a GridSearchCV object
from sklearn.model_selection import GridSearchCV

grid_search = GridSearchCV(rf_model, param_grid, cv=10, n_jobs=-1)

# Fit the model to the training data
grid_search.fit(X_train_encoded, y_train)

# Get the best model from the grid search
best_rf_model = grid_search.best_estimator_

best_rf_model.score(X_train_encoded, y_train), best_rf_model.score(X_test_encoded, y_test)

# Print the best hyperparameters
print(f'Best Hyperparameters: {grid_search.best_params_}')

# Evaluate the model on the test set
from sklearn.metrics import mean_squared_error



y_pred = best_rf_model.predict(X_test_encoded)
mse = mean_squared_error(y_test, y_pred)


print(f'Optimal MSE on Test Set: {mse}')
print(y_pred[:5])

y_pred_unseen = best_rf_model.predict(X_encoded_unseen)

print(y_pred_unseen[:5])

"""## Evaluating model performances like underfitting and overfitting with Learning Curves"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve
from sklearn.ensemble import RandomForestRegressor

# Generate some example data or load your dataset
# X, y = ...

# Create a RandomForestRegressor
# model = RandomForestRegressor(n_estimators=100, random_state=42)

# Define learning curve parameters
train_sizes, train_scores, test_scores = learning_curve(
    best_rf_model, X_encoded, df['Purchase_Amount'], cv=5, scoring='neg_mean_squared_error',
    train_sizes=np.linspace(0.1, 1.0, 10)
)

# Calculate mean and standard deviation of training and test scores
train_mean = -np.mean(train_scores, axis=1)
train_std = np.std(train_scores, axis=1)
test_mean = -np.mean(test_scores, axis=1)
test_std = np.std(test_scores, axis=1)


print(train_sizes)
print(train_mean)
print(train_std)
print(test_mean)
print(test_std)

# Plot the learning curve
plt.figure(figsize=(10, 6))
plt.plot(train_sizes, train_mean, label='Training Score', marker='o')
plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.15)

plt.plot(train_sizes, test_mean, label='Cross-Validation Score', marker='o')
plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, alpha=0.15)

plt.title('Learning Curve for RandomForestRegressor')
plt.xlabel('Number of Training Examples')
plt.ylabel('Negative Mean Squared Error')
plt.legend(loc='best')
plt.grid(True)
plt.show()

# Identify outliers

# Calculate residuals

residuals_test = y_test - y_pred  # or y_test - y_pred_unseen

# Use a method like Z-score to identify potential outliers
z_scores_test = (residuals_test - np.mean(residuals_test)) / np.std(residuals_test)

# Set a threshold for considering a data point as an outlier
threshold = 3  # Adjust as needed

# Identify outliers
outliers = np.where(np.abs(z_scores_test) > threshold)[0]

# Print or visualize the indices of potential outliers
print("Indices of potential outliers:", outliers)