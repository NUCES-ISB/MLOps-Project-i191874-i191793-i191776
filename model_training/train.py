import os
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle
import mlflow
from sklearn.metrics import accuracy_score

os.system('dvc pull data/iris.data')  # Pull the data from DVC remote

# Load the iris dataset from local DVC cache
iris = datasets.load_iris()

X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

sklearn_model = LogisticRegression(random_state=0).fit(X_train, y_train)

# Log model
mlflow.sklearn.log_model(sklearn_model, "model")

# Log metrics
train_accuracy = sklearn_model.score(X_train, y_train)
test_accuracy = sklearn_model.score(X_test, y_test)
mlflow.log_metric("train_accuracy", train_accuracy)
mlflow.log_metric("test_accuracy", test_accuracy)

# Save model
model_path = "../models/model.pkl"
with open(model_path, 'wb') as f:
    pickle.dump(sklearn_model, f)

mlflow.end_run()
