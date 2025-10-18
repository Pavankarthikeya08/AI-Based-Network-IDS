import streamlit as st
import pandas as pd
import joblib
import os
import numpy as np
from utils import FEATURE_COLS

st.set_page_config(page_title='IDS Demo', layout='wide')
st.title('AI-Based Network IDS — Demo')

model_path = os.path.join(os.getcwd(), 'ids_model.joblib')
if not os.path.exists(model_path):
    st.warning('Model not found. Run train.py to generate ids_model.joblib or use sample_flows.csv')

uploaded = st.file_uploader('Upload flows CSV (columns: {})'.format(','.join(FEATURE_COLS)), type=['csv'])
if uploaded is None:
    if st.button('Load sample data'):
        sample_path = os.path.join(os.getcwd(), 'sample_flows.csv')
        if os.path.exists(sample_path):
            df = pd.read_csv(sample_path)
        else:
            st.error('sample_flows.csv not found')
            st.stop()
    else:
        st.info('Upload a CSV or load sample data to continue')
        st.stop()
else:
    df = pd.read_csv(uploaded)

missing = [c for c in FEATURE_COLS if c not in df.columns]
if missing:
    st.error('Missing columns: {}'.format(missing))
    st.stop()

bundle = joblib.load(model_path)
model = bundle['pipeline']
feature_cols = bundle['feature_cols']
X = df[feature_cols]

scores = model.predict_proba(X)[:,1]
preds = model.predict(X)

df_out = df.copy()
df_out['attack_score'] = scores
df_out['pred_label'] = np.where(preds==1, 'ATTACK', 'BENIGN')

st.subheader('Top suspicious flows')
st.dataframe(df_out.sort_values('attack_score', ascending=False).head(100))

st.subheader('Download scored CSV')
csv = df_out.to_csv(index=False).encode()
st.download_button('Download results', data=csv, file_name='scored_flows.csv')

if 'label' in df.columns:
    from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
    y_true = (df['label'] != 'BENIGN').astype(int)
    st.subheader('Evaluation on uploaded data')
    st.text(classification_report(y_true, preds, digits=4))
    st.write('Confusion matrix:')
    st.write(confusion_matrix(y_true, preds))
    try:
        st.write('ROC-AUC:', roc_auc_score(y_true, scores))
    except:
        pass
