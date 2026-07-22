import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv(r"C:\Users\Ahmad Ali\Downloads\Election-Campaign-Analysis--main\Election-Campaign-Analysis--main\data\election_dataset_fixed_10states.csv")



# Only winners
df = df[df["Winner"]=="Yes"]


# Features (Party removed)
X = df[[
    "State",
    "Constituency",
    "Age",
    "Education",
    "Criminal_Cases",
    "Assets",
    "Liabilities",
    "Campaign_Spending",
    "Registered_Electors",
    "Urban_Rural",
    "Incumbent"
]]

# Target
y = df["Party"]


categorical = [
    "State",
    "Constituency",
    "Education",
    "Urban_Rural",
    "Incumbent"
]

numeric = [
    "Age",
    "Criminal_Cases",
    "Assets",
    "Liabilities",
    "Campaign_Spending",
    "Registered_Electors",
]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", SimpleImputer(strategy="median"), numeric),
        ("cat",
         Pipeline([
             ("imputer",SimpleImputer(strategy="most_frequent")),
             ("onehot",OneHotEncoder(handle_unknown="ignore"))
         ]),
         categorical)
    ]
)

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42
)

pipe = Pipeline([
    ("preprocessor",preprocessor),
    ("classifier",model)
])

X_train,X_test,y_train,y_test=train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

pipe.fit(X_train,y_train)

pred=pipe.predict(X_test)

accuracy = accuracy_score(y_test, pred)

accuracy = round(accuracy * 100, 2)

print("Model Accuracy:", accuracy, "%")

# Save model
joblib.dump(pipe, "model.pkl")

# Save accuracy
joblib.dump(accuracy, "accuracy.pkl")