# ⚙️ Adaptive Resource Allocation Dashboard

> AI-powered real-time resource optimization system using Reinforcement Learning (Q-Learning), intelligent scheduling, and interactive dashboard analytics.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![AI](https://img.shields.io/badge/AI-Q--Learning-green)
![Status](https://img.shields.io/badge/Project-Active-success)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🚀 Overview

Adaptive Resource Allocation Dashboard is a smart system simulation platform that dynamically manages CPU and memory resources using a Reinforcement Learning agent.

Instead of static allocation, the system continuously monitors workload conditions, detects inefficiencies, and learns better allocation strategies over time.

This project demonstrates the combination of:

- Artificial Intelligence  
- Reinforcement Learning  
- Operating System Concepts  
- Resource Scheduling  
- Real-Time Monitoring  
- Data Visualization  
- Dashboard Engineering  

---

## ✨ Key Features

### 🧠 Intelligent Allocation Engine

- Q-Learning based decision system  
- 100 environment states (CPU × Memory buckets)  
- 5 dynamic allocation actions  
- Epsilon-greedy exploration strategy  
- Self-improving resource policy  
- Reward-driven optimization  

### 📊 Real-Time Dashboard

- Live CPU monitoring  
- Live Memory monitoring  
- Reward tracking  
- Health score system  
- Efficiency metrics  
- Interactive Plotly charts  

### ⚙️ System Simulation

- Multiple simulated running processes  
- Heavy Load mode  
- Idle mode  
- Burst mode  
- Balanced mode  
- Priority scheduling mode  
- Static baseline comparison  

### 🛡 Reliability Monitoring

- Bottleneck detection  
- Overload alerts  
- Starvation warnings  
- Stability scoring  
- Performance anomaly detection  

### 📄 Reporting & Logs

- CSV logging  
- Historical analytics  
- Professional PDF report export  
- Downloadable summaries  

---

## 🧰 Tech Stack

| Category | Tools |
|--------|------|
| Language | Python |
| Frontend | Streamlit |
| Data Processing | Pandas, NumPy |
| Monitoring | Psutil |
| Visualization | Plotly |
| Reports | ReportLab |
| AI Logic | Q-Learning |

---

## 🧠 Reinforcement Learning Logic

The AI agent learns optimal allocation decisions using rewards and penalties.

### State Space

- CPU usage buckets (0–9)  
- Memory usage buckets (0–9)  

**Total States = 100**

### Actions

1. No Change  
2. Increase CPU  
3. Increase Memory  
4. Reduce CPU  
5. Reduce Memory  

### Reward Strategy

- Penalize overload  
- Penalize idle waste  
- Reward balanced utilization  
- Improve long-term efficiency  

---

## 📷 Dashboard Modules

### 📊 Live Performance

- CPU metrics  
- Memory gauges  
- Reward trends  
- Health score  

### 🗂 Process Monitoring

- Running simulated processes  
- Priority levels  
- Resource allocation visibility  

### 📈 Analytics

- Average load  
- Peak load  
- Efficiency trends  
- Historical summaries  

### 🧠 RL Brain

- Q-table heatmap  
- AI decision intelligence visualization  

---

## 📁 Project Structure

```bash
adaptive-resource-allocation-dashboard/
│── app2.py
│── allocation_logs.csv
│── requirements.txt
│── README.md
│── assets/
│── reports/


git clone https://github.com/ArnavGodara/adaptive-resource-allocation-dashboard.git

cd adaptive-resource-allocation-dashboard

pip install -r requirements.txt

streamlit run app2.py