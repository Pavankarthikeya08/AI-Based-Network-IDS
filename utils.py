import pandas as pd
import numpy as np

def binary_label_from_text(label_series):
    return (label_series != 'BENIGN').astype(int)

FEATURE_COLS = [
    'duration','packets','src_bytes','dst_bytes','bytes_per_sec',
    'protocol','flags_syn','flags_ack','dst_port','failed_logins'
]
