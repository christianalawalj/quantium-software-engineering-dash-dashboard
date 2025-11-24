Quantium Software Engineering – Dash Dashboard

Hi! I’m Christiana T. Lawal, and this repository holds my work for the Quantium Software Engineering Job Simulation on Forage.
This project walks through how software engineers at Quantium support their data teams — from environment setup to building clean, interactive dashboards in Python.

  Project Overview

This simulation mirrors the workflow of software engineers who support Quantium’s data analytics teams.  
The tasks include:

 The simulation is structured around a realistic engineering workflow, and I’ve been documenting each step as I complete it. So far, I’ve focused on getting my development environment set up properly and preparing the foundation for the dashboard.
✔️ Task 1 — Local Setup & Environment Configuration
For the first task, I:
Forked and cloned the starter Quantium repository
Created and activated a Python virtual environment
Installed all the core dependencies: dash, dash[testing], pandas, etc.
Cleaned up the repo by adding a proper .gitignore
Generated a fresh requirements.txt
Committed everything with clear messages and pushed to GitHub 

 As I continue the simulation, I’ll be working on:
Cleaning and preparing a messy dataset
Building an interactive dashboard using Dash & Plotly
Styling + improving UI components
Adding callback functions for interactivity
Writing lightweight tests using the dash testing framework
I’ll keep updating this repo as I complete each part.

The repository will be updated as each task is completed.
Technologies Used
Python 3.11
Dash
Plotly
Pandas
Virtual Environments
Git / GitHub
Testing tools included in dash[testing]


1. Clone the project
git clone https://github.com/christianalawalj/quantium-software-engineering-dash-dashboard.git

 2. Enter project folder
cd quantium-software-engineering-dash-dashboard

3. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate    # macOS & Linux

4. Install dependencies
pip install -r requirements.txt

5. Run the Dash app (once app.py is added)
python app.py

---

 📁 Repository Structure
```bash
quantium-software-engineering-dash-dashboard/
│
├── .venv/                # Virtual environment (ignored by Git)
├── requirements.txt      # Project dependencies
├── .gitignore            # Git ignore file
└── (future) app.py       # Dash application
└── (future) data/        # Cleaned & processed datasets


