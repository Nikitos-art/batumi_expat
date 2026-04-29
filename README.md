# ☕ Batumi Cafés Project

## 📌 Description
A small project that monitors Google data to discover newly opened cafés in Batumi. The goal is to automate the process of collecting, storing, and presenting local business information.

---

## ⚙️ Tech Overview

### 🔍 Data Collection
- Uses **Beautiful Soup**, **lxml**, **Selenium**, and other third-party libraries  
- Scrapes and parses Google data to collect café information  
- Performs an initial full scrape, followed by automated checks for newly opened cafés  
- Stores data in **MongoDB**  
- Runs locally using **Docker**

### 🌐 Backend & Web App
- Built with **Flask**  
- Retrieves data from the database and serves it via structured routes  
- Renders content using frontend templates  
- Serves static files for the UI  

---

## 📄 Pages / Features

### 🏠 Main Page
- Basic Batumi-related information (e.g., flight info)  
- Additional sections planned  

### 📂 Categories
- ☕ Cafés  
- 🏢 Apartments for Rent  
- 💈 Barber Shops  
- 🏋️ Gyms  
- 👩‍👧 For Kids & Moms  

---

## 🧠 Notes
This project is an ongoing experiment focused on web scraping, automation, and building a simple data-driven web application. The structure is designed to be easily extendable to other categories beyond cafés.

## Docker local launch ###
docker compose up -d