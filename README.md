# EcoSphere - Sustainability Management Platform

**EcoSphere** is a modern, responsive sustainability tracker and management platform designed to encourage eco-friendly habits and digitize individual environmental accountability. With a rich green glassmorphic design system and smooth charts, it offers users a comprehensive panel to track resource consumption, calculate carbon emissions, plant trees, and fulfill custom green milestones.

EcoSphere was developed with clean, modular architecture, rendering it highly scalable and production-ready for national-level hackathons.

---

## 👥 Team

**Team Name:** Hackers 2.0

| Name | Role |
|------|------|
| Abishna K. | Team Lead |
| Iniya S. | Team Member |
| Aarthi P. | Team Member |
| Femina N. | Team Member |

---

## 📌 Problem Statement

Sustainability efforts are scattered and invisible. Water, electricity, and waste usage are often not recorded in one place, making it difficult for individuals to understand their overall environmental footprint.

Without trends or historical data, users have limited visibility into whether their daily habits are improving or getting worse. Green actions such as tree planting may also go unrecorded, resulting in a lack of milestones, goals, and motivation to stay consistent.

**EcoSphere addresses this problem by providing a single platform to measure, track, and improve individual sustainability activities.**

---

## 💡 Solution Overview

EcoSphere is a smart sustainability tracking platform that brings multiple environmental metrics together in one place.

The platform allows users to track water usage, electricity consumption, waste management, tree plantation activities, and carbon footprint. A smart dashboard provides live charts and activity history, while goals and milestones encourage users to maintain sustainable habits consistently.

---

## 📊 PPT

**PPT Link:**  

https://drive.google.com/file/d/1xfgS6Hm_hWNDYGD_8EUCsmmtoNX5UzIr/view?usp=drive_link
---

## 🎥 Live Demonstration

[Watch EcoSphere Demo](https://drive.google.com/file/d/13UQd-CXRra6oBKAzrS2XBy2sbAtlVhAM/view?usp=drivesdk)

---

## 🌟 Key Features

1. **Secure Authentication & Session Management**: Dedicated login and registration screens with hashed credentials using `Werkzeug` secure helpers.
2. **Dynamic Dashboard Overview**:
   - **Daily Eco Tips**: Interactive advice banner that cycles daily based on current dates.
   - **Key Aggregates**: Core stats counting logged water, electricity, waste, and planted trees.
   - **Interactive Charts**: Responsive timeline trends (Emissions History and Waste Category distribution).
3. **Dedicated Resource Trackers**:
   - 💧 **Water Usage Tracker**: Record liter usage, view average rates, and view bar graph logs.
   - ⚡ **Electricity Tracker**: Log power consumption in kWh alongside interactive timeline charts.
   - 🗑️ **Waste Management (Reduce, Reuse, Recycle)**: Track household waste diversion categorized by actions with associated donut charts.
   - 🌱 **Tree Plantation Tracker**: Record tree saplings planted (quantity, species, and planting sites) alongside a species variety bar chart.
4. **Carbon Footprint Calculator**:
   - A multi-step quiz wizard capturing weekly transit distances, household energy utility logs, and recycling coefficients.
   - Yields carbon emissions breakdown (Transport, Energy, Waste) measured against local targets.
5. **Gamified Profile & Goals**:
   - Eco-milestones detailing lifetime ecological contributions.
   - Custom progress goals (e.g. planting 5 trees, diverting 20kg waste) updating dynamically as trackers receive logs.

---

## 💻 Tech Stack

- **Backend**: Python 3.x, Flask, Flask-SQLAlchemy, Flask-Login, PyMySQL, Python-dotenv
- **Frontend**: HTML5 (Semantic Structure), CSS3 (Custom Glassmorphism styling system, transitions, CSS variables), JavaScript (ES6, AJAX trends loaders, Quiz Pagination)
- **Visual Libraries**: Chart.js (CDNs for analytics), Lucide Icons (CDN outline icons)
- **Database**: MySQL (production-ready) with a dynamic local development fallback to SQLite (`ecosphere.db`) when MySQL credentials are not configured in environment files.

---

## 📁 Directory Structure

```text
ecosphere/
│
├── ecosphere/                  # Main application package
│   ├── __init__.py            # Package initialization (Blueprints & DB setup)
│   ├── config.py              # Dynamic configuration & Fallbacks
│   ├── models.py              # SQLAlchemy database model structures
│   ├── utils.py               # Calculation engines and tip dictionaries
│   ├── routes.py              # Front-facing views controller
│   ├── api.py                 # REST API JSON data providers
│   │
│   ├── static/                # Static assets folder
│   │   ├── css/
│   │   │   └── style.css      # Custom glassmorphic styling system
│   │   └── js/
│   │       └── main.js        # Dynamic front-end routines & Chart.js binders
│   │
│   └── templates/             # HTML Jinja2 template views
│       ├── base.html          # Global wrapper sidebar & layout
│       ├── login.html         # User sign-in
│       ├── register.html      # User registration
│       ├── dashboard.html     # Main stats & carbon history
│       ├── water.html         # Water logging & trends
│       ├── electricity.html   # Energy logging & trends
│       ├── waste.html         # Waste logging & doughnut breakdown
│       ├── tree.html          # Tree planting & species variety
│       ├── carbon.html        # Multi-step carbon quiz
│       └── profile.html       # Profile edit & gamified milestones
│
├── requirements.txt            # System dependencies manifest
├── .env.example                # Template configurations
├── schema.sql                  # Raw SQL setup script for MySQL
├── run.py                      # App entry point
└── README.md                   # Project documentation
```

---

## 🚀 Setup & Installation Instructions

Follow these steps to deploy and run EcoSphere locally:

### 1. Clone the Project

Open a command prompt in the workspace directory.

### 2. Set Up Virtual Environment

Create and activate a virtual environment to manage dependencies:

```bash
# Create environment
python -m venv venv

# Activate on Windows (cmd)
venv\Scripts\activate

# Activate on Windows (PowerShell)
.\venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

EcoSphere features dual database configurations:

- **Development (Zero-Config SQLite)**: By default, the application will create a local SQLite database named `ecosphere.db` in the project root if no MySQL configurations are provided. You can run the application immediately without database installations.
- **Production (MySQL)**:
  1. Ensure your MySQL server is running.
  2. Create a database called `ecosphere` (or let the app auto-create it).
  3. Copy `.env.example` to a new file named `.env`:
     ```bash
     copy .env.example .env
     ```
  4. Edit `.env` and set the `DATABASE_URL` line to your MySQL credentials:
     ```text
     DATABASE_URL=mysql+pymysql://username:password@localhost:3306/ecosphere
     ```
  5. The tables will auto-initialize upon launching the app, or you can import `schema.sql` manually.

### 5. Launch the Application

Run the entry point script:

```bash
python run.py
```

Open your browser and navigate to **`http://localhost:5000`** to interact with the application. Register a new user account to log in and start using the trackers.
