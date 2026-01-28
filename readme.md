# 🌍 Local Food Wastage Management System

## 📌 Project Overview
Food wastage is a serious global challenge — large quantities of edible food are discarded every day while many people struggle with food insecurity.

The **Local Food Wastage Management System** is a data-driven web application built to address this gap.  
It connects people and organizations who have surplus food with those who need it, using **Python, SQL, Data Analysis, and Streamlit**.

This is a **real-world, end-to-end Data Science project** that combines database management, analytics, visualization, and a fully functional web interface.

---

## 🎯 Problem Statement
Restaurants, grocery stores, and households often waste surplus food due to a lack of structured redistribution systems.  
At the same time, NGOs and individuals face difficulty accessing food when needed.

This project aims to:
- Enable users to **list surplus food**
- Allow receivers to **discover and claim food nearby**
- Store and manage data efficiently using **SQL**
- Analyze food availability and demand patterns
- Present insights through an **interactive Streamlit dashboard**

---

## 🧠 Business Use Cases
- Reduce food wastage through efficient redistribution  
- Connect food providers and receivers at a local level  
- Support data-driven decision-making using analytics  
- Promote sustainability and social good  

---

## 🛠️ Tech Stack
- **Python** – Core application logic  
- **SQLite (SQL)** – Structured data storage  
- **Pandas & NumPy** – Data cleaning and analysis  
- **Streamlit** – Interactive web application  
- **Matplotlib & Plotly** – Data visualization  
- **SQLAlchemy** – Database connectivity  

---

## 📂 Project Structure
Local-Food-Wastage-Management-System/
│
├── app.py # Main Streamlit application
├── requirements.txt # Project dependencies
├── README.md # Documentation
│
├── database/
│ └── food_waste.db # SQLite database
│
├── data/
│ ├── providers_data.csv
│ ├── receivers_data.csv
│ ├── food_listings_data.csv
│ └── claims_data.csv
│
├── src/
│ ├── db.py # Database schema & connection
│ ├── queries.py # SQL queries & CRUD operations
│ └── load_data.py # CSV data loader


---

## 📊 Dataset Description

### 🏪 Providers Dataset
Contains details of food providers such as restaurants and grocery stores.
- Provider ID  
- Name  
- Type  
- Address  
- City  
- Contact  

### 👥 Receivers Dataset
Stores information about individuals or organizations receiving food.
- Receiver ID  
- Name  
- City  
- Contact  

### 🍱 Food Listings Dataset
Stores details of available food items.
- Food ID  
- Food Name  
- Quantity  
- Expiry Date  
- Provider ID  
- Location  
- Food Type  
- Meal Type  

### 📦 Claims Dataset
Tracks food claims made by receivers.
- Claim ID  
- Food ID  
- Receiver ID  
- Status  
- Timestamp  

---

## 🔄 Project Workflow
1. Load and clean datasets using Pandas  
2. Store structured data in an SQL database  
3. Implement CRUD operations for food listings and receivers  
4. Perform data analysis on food availability and claims  
5. Generate insights and trends using visualizations  
6. Provide a user-friendly interface through Streamlit  

---

## 📈 Key Analytics & Insights
- Total food available across all providers  
- Most commonly available food types  
- Claim status distribution  
- Top receivers based on number of claims  
- Food claim trends over time  
- City-wise food availability  

---

## 👥 Application Features

### 🔐 Authentication
- User login and signup  
- Secure session handling  

### 🍱 Food Provider
- Add food listings  
- Update real-time food availability  

### 🤝 Food Receiver
- Create and update receiver profile  
- View food available in their city  
- Claim food items  

### 📊 Dashboard & EDA
- Live metrics and KPIs  
- Interactive charts and graphs  
- Trend and pattern analysis  

---

🌱 Future Enhancements
Role-based access (Admin / Provider / Receiver)

Location-based food search using maps

Notifications for food availability

Cloud database deployment

Advanced analytics and forecasting

🤝 Conclusion
This project demonstrates how Data Science, SQL, and Web Applications can be combined to solve a meaningful real-world problem.

The Local Food Wastage Management System is not just a dashboard — it is a complete, scalable, and socially impactful solution that highlights strong skills in:
Python, SQL, Data Analysis, EDA, and Streamlit development.

