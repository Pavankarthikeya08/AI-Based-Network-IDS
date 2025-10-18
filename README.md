# 🛡️ AI-Based Network IDS 

This project demonstrates an **AI-based Network Intrusion Detection System (IDS)** that predicts network attacks from flow data. Users can upload a CSV with network flow features and get predictions using a pre-trained machine learning model.

---

## 🔹 Features

- Predict network attacks using a **Random Forest model**.
- Supports CSV input with required features.
- Generates **predictions** and allows **CSV download**.
- Web interface using **Streamlit**.

---

## 🗂️ Dataset Requirements

The uploaded CSV file should contain the following columns:

| Feature | Description |
|---------|-------------|
| `duration` | Duration of the flow |
| `packets` | Number of packets |
| `src_bytes` | Bytes sent from source |
| `dst_bytes` | Bytes sent to destination |
| `bytes_per_sec` | Flow throughput |
| `protocol` | Protocol type (e.g., TCP/UDP) |
| `flags_syn` | SYN flag |
| `flags_ack` | ACK flag |
| `dst_port` | Destination port |
| `failed_logins` | Number of failed login attempts |

Optional: if a `Label` column exists, it will be ignored during prediction.

---

## 🖥️ Using the App

1. Open the Streamlit app in your browser.  
   ![Streamlit Home](https://github.com/user-attachments/assets/e4f2f05b-a59d-4698-9130-5ec05a07a550)  

2. Upload a CSV file containing network flow data.  
   ![Upload CSV](https://github.com/user-attachments/assets/d3b320e8-b84e-4ad7-8562-eed373fc729d)  

3. View the generated predictions and download as CSV.  
   ![Predictions Table](https://github.com/user-attachments/assets/90b6e4f9-20bb-4f20-b3bf-1907048622ea)  

---

## 📝 Output Example

| duration | packets | src_bytes | dst_bytes | bytes_per_sec | protocol | flags_syn | flags_ack | dst_port | failed_logins | Prediction |
|----------|---------|-----------|-----------|---------------|---------|-----------|-----------|----------|---------------|------------|
| 5        | 2       | 100       | 200       | 60            | 1       | 1         | 1         | 22       | 1             | 1          |

- ✅ **Prediction = 1** → attack detected  
- ⚪ **Prediction = 0** → normal flow

---
