#!/usr/bin/env python3
import argparse
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib
from utils import FEATURE_COLS, binary_label_from_text

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True, help='Input flows CSV for training')
parser.add_argument('--out-model', default='ids_model.joblib')
args = parser.parse_args()

df = pd.read_csv(args.input)
feature_cols = [c for c in FEATURE_COLS if c in df.columns]
X = df[feature_cols].copy()
if 'label' in df.columns:
    y = binary_label_from_text(df['label'])
else:
    raise SystemExit('Input CSV must include a "label" column for training')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

num_cols = [c for c in feature_cols if c != 'protocol']
cat_cols = ['protocol'] if 'protocol' in feature_cols else []

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), num_cols),
    ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
])

clf = Pipeline([
    ('pre', preprocessor),
    ('clf', RandomForestClassifier(n_estimators=200, random_state=0, n_jobs=-1))
])

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
try:
    y_proba = clf.predict_proba(X_test)[:,1]
    print('ROC-AUC:', roc_auc_score(y_test, y_proba))
except Exception:
    pass
print(classification_report(y_test, y_pred))
print('Confusion matrix:')
print(confusion_matrix(y_test, y_pred))

joblib.dump({'pipeline': clf, 'feature_cols': feature_cols}, args.out_model)
print('Saved model to', args.out_model)
