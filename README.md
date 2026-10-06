# Smart Finance Dashboard

Smart Finance Dashboard is a Python‑based personal expense tracking and analytics app.  
It uses **Pandas** and **Matplotlib** for data processing and visualization, and **Streamlit** for an interactive web UI.

The app lets you:

- Add and store daily expenses in a CSV file  
- View key metrics (total spent, number of entries, average per expense)  
- Explore **category‑wise** and **monthly** spending trends  
- Detect high‑spending days using simple statistics  
- Use a dark, modern dashboard theme configured via `.streamlit/config.toml`  

---
<img width="1903" height="877" alt="Screenshot 2026-04-05 191337" src="https://github.com/user-attachments/assets/81704c15-f468-4be5-8b63-255eebed8fb2" />



## 🔗 Repository

GitHub: https://github.com/pb3890/Smart_finance_Dashboard  

---

## 🔧 Tech Stack

- Python 3.x  
- [Streamlit](https://streamlit.io/) – web UI  
- [Pandas](https://pandas.pydata.org/) – data handling and aggregation  
- [Matplotlib](https://matplotlib.org/) – charts and plots  

---

## 📁 Project Structure

```text
Smart_finance_Dashboard/
├── app.py                 # Streamlit dashboard (main entry point)
├── expense_app.py         # CLI version (optional)
├── data/
│   └── expenses.csv       # Expense data (CSV)
└── .streamlit/
    └── config.toml        # Streamlit theme configuration
```

- `app.py` – main frontend, includes:
  - Dashboard page with KPIs and recent transactions  
  - Add Expense page with form  
  - Analytics page with category breakdown, monthly trend, and high‑spending days  
- `expense_app.py` – simple command‑line version of the tracker (for terminal use).  
- `data/expenses.csv` – where expenses are stored; if missing, the app creates it automatically.  
- `.streamlit/config.toml` – defines a dark, professional theme for the app.

---

## ▶️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/pb3890/Smart_finance_Dashboard.git
cd Smart_finance_Dashboard
```

### 2. (Optional) Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows

# On macOS / Linux:
# source venv/bin/activate
```

### 3. Install dependencies

If you add a `requirements.txt`, use:

```bash
pip install -r requirements.txt
```

Otherwise:

```bash
pip install streamlit pandas matplotlib
```

---

## Run the Streamlit Dashboard

From the project root:

```bash
streamlit run app.py
```

Streamlit will start a local server and show a URL such as:

```text
http://localhost:8501
```

Open that URL in your browser to use the dashboard.

---

## CLI Version (Optional)

You can also run the simple terminal‑based tracker:

```bash
python expense_app.py
```

This version lets you add and view expenses via a text menu, using the same CSV file.

---

## Features

### Dashboard

- Overall **total spent**, **number of entries**, **average per expense**, and **amount spent in the current month**  
- Table of the **most recent transactions**, sorted by date  

### Add Expense 

- Form with:
  - Date  
  - Amount  
  - Category (Food, Transport, Shopping, etc.)  
  - Description  
- On submission, the expense is appended to `data/expenses.csv`
-
- <img width="1898" height="872" alt="Screenshot 2026-04-05 191445" src="https://github.com/user-attachments/assets/153e5358-5fd6-433c-850a-f0d214bcaa41" />


### Analytics

- **By Category**  
  - Bar chart of total amount per category  
  - Summary table of category amounts  

- **Monthly Trend**  
  - Line chart of total spending per month  
  - Uses Pandas `groupby` on the `Month` period  

- **High‑Spending Days**  
  - Computes daily totals and highlights days where spending is greater than 2× average daily spend  

---
<img width="1897" height="870" alt="Screenshot 2026-04-05 191529" src="https://github.com/user-attachments/assets/eecbb89a-572b-4c19-9105-e04abffa5f16" />

<img width="1899" height="869" alt="Screenshot 2026-04-05 191631" src="https://github.com/user-attachments/assets/47fcb830-5686-4d06-8cdd-e88be818b729" />

## Theming

The dark theme is configured in `.streamlit/config.toml`:

```toml
[theme]
base="dark"
primaryColor="#2563EB"
backgroundColor="#020617"
secondaryBackgroundColor="#0F172A"
textColor="#E5E7EB"
font="sans serif"
```

Streamlit loads this automatically when you run `streamlit run app.py`.

---

# 📈 Possible Extensions

- Monthly and per‑category budget limits with warnings  
- CSV upload for importing bank/UPI statements  
- Export reports as PDF or CSV  
- Simple ML‑based category prediction for new transactions  

---

# Author

Created by **Princess Bajpai (pb3890)**  

- GitHub: [@pb3890](https://github.com/pb3890)

