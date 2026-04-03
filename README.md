# Logsentinel

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![AI-Powered](https://img.shields.io/badge/AI-BERT%20%2B%20LLM-red.svg)]()

An advanced, multi-layered log analysis system that leverages **Regex**, **Machine Learning (BERT)**, and **Large Language Models (LLMs)** to classify system logs and identify security breaches in real-time.

---

##  Project Overview

This project simulates a Security Operations Center (SOC) monitoring environment. Unlike traditional static analyzers, this system utilizes a hybrid pipeline to ensure that the LLM captures even obfuscated or "zero-day" log patterns when traditional rules fail.

Key Capabilities:

- **Multi-Stage Classification**: Cascading logic from fast Regex to deep LLM analysis.  
- **Behavioral Tracking**: State-aware detection for brute-force patterns across multiple log entries.
- **Automated Reporting**: Generates audit-ready Excel reports with statistical summaries.  
- **Label Normalization**: A dedicated abstraction layer to ensure consistent taxonomy across diverse AI models.  

The system uses a **multi-layered classification pipeline** to ensure accuracy and robustness.

---
## System Architecture

The system operates on a **Tiered Inference Logic**:

1.  **Level 1 (Regex):** Instant matching for known signatures (Low Latency).
2.  **Level 2 (BERT):** Semantic analysis for logs that resemble known threats but lack exact signatures.
3.  **Level 3 (LLM):** Cognitive reasoning via LLaMA 3 for ambiguous or complex anomalies (High Accuracy).

---

## 🧠 Core Features

### 🔍 The Hybrid Pipeline
| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Fast Path** | Python Regex | High-speed filtering of standard system events. |
| **ML Path** | BERT + Logistic Regression | Understanding context and intent within log strings. |
| **Deep Path** | LLaMA 3 (via Groq) | Reasoning through complex, novel, or suspicious logs. |

---
### 🛡️ Threat Intelligence
The system is pre-configured to identify:
* **Authentication Attacks:** Failed logins and IP-based brute-force correlation.
* **Access Anomalies:** Unauthorized privilege escalation attempts.
* **Injections:** Suspicious string patterns (SQLi, XSS) hidden in logs.
---

## 📁 Project Structure

```text
.
├── processor_regex.py # Rule-based classification
├── processor_bert.py # ML-based classification (BERT + Logistic Regression)
├── processor_llm.py # LLM-based classification (Groq API)
├── classify.py # Main pipeline + threat detection + reporting
├── models/ # Saved ML models
├── resources/ # Input/output files
├── training/ # Model training scripts
├── .env # API keys (ignored)
├── .gitignore
└── README.md
```
---

## ⚙️ Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Setup Environment Variables
Create a .env file in the root directory:
````bash
GROQ_API_KEY=your_api_key_here
````
### 4. Run the Project
```bash
python classify.py
```

---

## 📥 Input Format

Provide a CSV file inside the `resources/` folder with the following structure:

| source        | log_message |
|--------------|------------|
| ModernCRM     | Failed login attempt for user admin |

---

## 📤 Output

After running the project, a file named:
resources/security_report.xlsx


will be generated.

### Excel Report Structure

#### 📄 Sheet 1: All Logs
- Contains all input logs with predicted labels  

#### 🚨 Sheet 2: Threat Logs
- Contains only suspicious/malicious logs  

#### 📊 Sheet 3: Summary
- Count of each label  

---

##  Classification Labels

The system classifies logs into the following categories:

- `failed_login`  
- `brute_force_attempt`  
- `possible_attack`  
- `suspicious_activity`  
- `normal_activity`  
- `system_event`  

---

##  How It Works

1. **Regex Layer**
   - Quickly classifies known patterns  
   - Handles structured logs efficiently  

2. **ML Layer (BERT + Logistic Regression)**
   - Converts logs into embeddings  
   - Classifies based on trained model  

3. **LLM Layer (Groq + LLaMA)**
   - Handles ambiguous or unseen logs  
   - Acts as fallback  

4. **Brute Force Detection**
   - Tracks failed attempts per IP  
   - Flags repeated failures as attacks  

5. **Label Normalization**
   - Ensures consistent output across all layers  

---

## Future Improvements

- Real-time log monitoring (streaming logs)  
- Dashboard visualization using Streamlit  
- Integration with SIEM tools  
- Improved ML model with security-focused dataset  

---

## Disclaimer

This project is built for **educational purposes only** and demonstrates log classification and basic threat detection techniques.

---

## Author

**Jay Panchal**
