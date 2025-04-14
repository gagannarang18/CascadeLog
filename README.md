
# ⚡ CascadeLog 

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.22+-orange)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

**Enterprise log analysis platform** that automatically categorizes system logs and generates actionable insights.

![CascadeLog Demo](https://github.com/gagannarang18/Cassy/blob/main/resources/image.png) 

## 🌟 Key Features

- **Automatic log classification** with high accuracy
- **Multi-source support** (servers, networks, applications)
- **Interactive dashboard** with visual analytics
- **Exportable reports** in CSV format
- **REST API** for integration with other systems

## 🛠️ Tech Stack

| Component      | Technology |
|----------------|------------|
| Backend        | FastAPI    |
| Frontend       | Streamlit  |
| Core Logic     | Python 3.9 |
| NLP Processing | BERT       |
| Fallback       | GroqAI API |

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Git

### Installation
```bash
# Clone repository
git clone https://github.com/gagannarang18/CascadeLog.git
cd CascadeLog

# Install dependencies
pip install -r requirements.txt


## 🚀 Running the Application

### Method 1: Dual Terminal Setup
```bash
# Terminal 1: Start FastAPI backend (http://localhost:8000)
 uvicorn server:app --reload  

# Terminal 2: Start Streamlit frontend (http://localhost:8501)
streamlit run app.py


